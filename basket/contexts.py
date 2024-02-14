from django.conf import settings
from django.shortcuts import get_object_or_404
from edible_products.models import EdibleProduct
from profiles.models import Profile
from decimal import Decimal

def basket_contents(request):
    basket_items = []
    total = Decimal('0.00')
    product_count = 0
    basket = request.session.get('basket', {})

    # Define weight to price mapping
    weight_price_mapping = {
        '100': Decimal('3.50'),
        '400': Decimal('7.00'),
        '800': Decimal('11.00'),
    }

    for item_key, item_data in basket.items():
        parts = item_key.split('-')
        item_id_str = parts[0]
        flavour = 'Default' if len(parts) < 3 else parts[1]
        weight_str = '400' if len(parts) < 2 else parts[-1]  # Default weight
        weight = Decimal(weight_str)

        try:
            item_id = int(item_id_str)
            product = get_object_or_404(EdibleProduct, pk=item_id)
            quantity = item_data.get('quantity', 0) if isinstance(item_data, dict) else item_data

            # Get price for the specified weight
            price = weight_price_mapping.get(weight_str, product.price)

            subtotal = Decimal(quantity) * price
            total += subtotal
            product_count += quantity

            basket_items.append({   
                'item_id': item_id,
                'quantity': quantity,
                'flavour': flavour,
                'weight': weight_str,
                'product': product,
                'price': price,
                'subtotal': subtotal,
            })

        except ValueError:
            continue

    if not basket:  # Check if the basket is empty
        delivery = Decimal('0.00')  # Set delivery charge to zero if basket is empty
    else:
        delivery = Decimal(settings.DEFAULT_DELIVERY_CHARGE)
    
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            if user_profile.is_subscribed:
                delivery = Decimal('0.00')
        except Profile.DoesNotExist:
            pass
    grand_total = total + delivery

    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context
