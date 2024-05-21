from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal
from core.models import CommonProduct
from edible_products.models import EdibleProduct, ProductWeightPrice
from profiles.models import Profile
from merch.models import MerchProduct, TextOption

def basket_contents(request):
    basket_items = []
    total = Decimal('0.00')
    product_count = 0
    basket = request.session.get('basket', {})

    for item_id, item_data in basket.items():
        common_product = get_object_or_404(CommonProduct, pk=item_id)
        product_type = common_product.product_type

        if product_type == 'edible':
            product = get_object_or_404(EdibleProduct, pk=item_id)
            if 'details' in item_data:
                weight_data = item_data['details']
                for weight, quantity in weight_data.items():
                    price = product.get_price_for_weight(int(weight))
                    subtotal = Decimal(quantity) * Decimal(price) if (quantity and price) else Decimal('0.00')
                    basket_items.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'subtotal': subtotal,
                        'weight': weight,
                    })
                    total += subtotal
                    product_count += quantity

        elif product_type == 'merch':
            product = get_object_or_404(MerchProduct, pk=item_id)
            if 'details' in item_data:
                text_option_data = item_data['details']
                for text_option_id, quantity in text_option_data.items():
                    text_option = get_object_or_404(TextOption, pk=text_option_id)
                    subtotal = Decimal(quantity) * Decimal(product.price)
                    basket_items.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price,
                        'subtotal': subtotal,
                        'text_option': text_option,
                    })
                    total += subtotal
                    product_count += quantity

    delivery = calculate_delivery(total, request.user)
    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': total + delivery,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context

def calculate_delivery(total, user):
    delivery = Decimal(settings.DEFAULT_DELIVERY_CHARGE) if total > Decimal('0.00') else Decimal('0.00')
    if user and user.is_authenticated:
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.is_subscribed:
            delivery = Decimal('0.00')
    return delivery
