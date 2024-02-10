from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.http import HttpRequest
from edible_products.models import EdibleProduct

class BasketView(View):
    def get(self, request, *args, **kwargs):
        basket_items = []
        total = 0
        product_count = 0
        basket = request.session.get('basket', {})

        for item_key, item_data in basket.items():
            parts = item_key.split('-')
            if len(parts) == 1:
                # This is for simple items or items without weight/flavour differentiation
                real_item_id = parts[0]
                edible_product = get_object_or_404(EdibleProduct, pk=real_item_id)
                quantity = item_data if isinstance(item_data, int) else item_data.get('quantity', 0)
            elif len(parts) == 3:
                # For items stored with weight and flavour differentiation
                real_item_id, flavour, weight = parts
                edible_product = get_object_or_404(EdibleProduct, pk=real_item_id)
                quantity = item_data.get('quantity', 0) if isinstance(item_data, dict) else item_data
            else:
                # Handle other unexpected formats or log an error
                continue

            subtotal = quantity * edible_product.price
            basket_items.append({
                'item_id': real_item_id,
                'quantity': quantity,
                'weight': weight if len(parts) == 3 else None,
                'flavour': flavour if len(parts) == 3 else None,
                'edible_product': edible_product,
                'subtotal': subtotal,
            })

            total += subtotal
            product_count += quantity

        is_subscriber = request.user.is_subscriber if hasattr(request.user, 'is_subscriber') else False
        delivery = 0 if is_subscriber else settings.DEFAULT_DELIVERY_CHARGE
        grand_total = delivery + total

        context = {
            'basket_items': basket_items,
            'total': total,
            'product_count': product_count,
            'delivery': delivery,
            'grand_total': grand_total,
        }

        return render(request, 'basket/basket.html', context)


class AddToBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        """Add a quantity of the specified product to the shopping basket."""
        quantity = int(request.POST.get('quantity'))
        weight = request.POST.get('weight', '400')  # Default weight to '400' if not specified
        flavour = request.POST.get('flavour')
        redirect_url = request.POST.get('redirect_url', reverse('view_basket'))

        basket = request.session.get('basket', {})

        # Create a composite key
        item_key = f"{item_id}-{flavour}-{weight}"

        if item_key in basket:
            basket[item_key]['quantity'] += quantity
        else:
            basket[item_key] = {'quantity': quantity, 'weight': weight, 'flavour': flavour}

        request.session['basket'] = basket
        request.session.modified = True

        return redirect(redirect_url)
