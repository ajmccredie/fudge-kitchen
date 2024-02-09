from django.conf import settings
from django.shortcuts import get_object_or_404
from edible_products.models import EdibleProduct

def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get('basket', {})

    for item_id, quantity in basket.items():
        edible_product = get_object_or_404(EdibleProduct, pk=item_id)
        total += quantity * edible_product.price
        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'edible_products': edible_product,
        })

    delivery = 3

    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery
    }

    return context