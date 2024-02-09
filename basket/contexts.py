from django.conf import settings
from django.shortcuts import get_object_or_404
from edible_products.models import EdibleProduct

def basket_contents(request):
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})

    for item_id, item_data in basket.items():
        if isinstance(item_data, int):  # Case for items without specified weight
            edible_product = get_object_or_404(EdibleProduct, pk=item_id)
            quantity = item_data
            total += quantity * edible_product.price
            product_count += quantity
            basket_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'edible_product': edible_product,
                'subtotal': quantity * edible_product.price,
            })
        else:  # Case for items with specified weight
            edible_product = get_object_or_404(EdibleProduct, pk=item_id)
            for weight, quantity in item_data['items_by_weight'].items():
                total += quantity * edible_product.price
                product_count += quantity
                basket_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'weight': weight,  # Include weight in the basket items
                    'edible_product': edible_product,
                    'subtotal': quantity * edible_product.price,
                })

    is_subscriber = request.user.is_subscriber if hasattr(request.user, 'is_subscriber') else False
    delivery = 0 if is_subscriber else 3

    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
