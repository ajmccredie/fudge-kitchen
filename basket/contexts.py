from django.conf import settings
from django.shortcuts import get_object_or_404
from edible_products.models import EdibleProduct

def basket_contents(request):
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})

    for item_key, item_data in basket.items():
        parts = item_key.split('-')
        
        item_id_str = parts[0]
        flavour = 'Default' if len(parts) < 3 else parts[1]
        weight = '400' if len(parts) < 2 else parts[-1]
        
        try:
            item_id = int(item_id_str)
            product = get_object_or_404(EdibleProduct, pk=item_id)
        except ValueError:
            continue
        
        if isinstance(item_data, dict):
            quantity = item_data.get('quantity', 0)
        elif isinstance(item_data, int):
            quantity = item_data
        else:
            continue
        
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity

        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'flavour': flavour,
            'weight': weight,
            'product': product,
            'subtotal': subtotal,
        })

    delivery = settings.DEFAULT_DELIVERY_CHARGE if not request.user.is_authenticated else 0
    grand_total = total + delivery

    context = {
        'basket_items': basket_items,
        'total': total,
        'grand_total': grand_total,
        'product_count': product_count,
        'delivery': delivery,
    }

    return context
