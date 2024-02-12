from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from .contexts import basket_contents
from decimal import Decimal, InvalidOperation
from edible_products.models import EdibleProduct, ProductWeightPrice

class BasketView(View):
    def get(self, request, *args, **kwargs):
        context_data = basket_contents(request)
        basket_items = context_data.get('basket_items', [])
        total = context_data.get('total', Decimal('0.00'))
        product_count = context_data.get('product_count')
        delivery = context_data.get('delivery')
        grand_total = context_data.get('grand_total')

        context = {
            'basket_items': basket_items,
            'total': total,
            'product_count': product_count,
            'delivery': delivery,
            'grand_total': grand_total,
        }
        print(f"The basket items the page should see: {basket_items}")
        print(f"The total in the context: {total}")
        return render(request, 'basket/basket.html', context)


class AddToBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        """Add a quantity of the specified product to the shopping basket."""
       # product = get_object_or_404(EdibleProduct, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        #weight = request.POST.get('weight', '400')  # Default weight to '400' if not specified
        flavour = request.POST.get('flavour')
        redirect_url = request.POST.get('redirect_url', reverse('view_basket'))

        product = get_object_or_404(EdibleProduct, pk=item_id)
        weight = int(request.POST.get('weight', '100'))  # Assuming weight is now an integer
        
        try:
            weight_price_obj = product.weight_prices.get(weight=weight)
            price = weight_price_obj.price
        except ProductWeightPrice.DoesNotExist:
            price = product.price

        basket = request.session.get('basket', {})

        # Create a composite key
        item_key = f"{item_id}-{flavour}-{weight}"

        if item_key in basket:
            basket[item_key]['quantity'] += quantity
            basket[item_key]['price'] = str(price) 
        else:
            basket[item_key] = {'quantity': quantity, 'weight': weight, 'flavour': flavour, 'price': str(price)}

        request.session['basket'] = basket
        request.session.modified = True

        print("Updated Basket:", request.session['basket'])
        return redirect(redirect_url)



class UpdateBasketView(View):
    def post(self, request, *args, **kwargs):
        item_id = str(kwargs['item_id'])
        quantity = int(request.POST.get('quantity'))

        basket = request.session.get('basket', {})

        print(f"Updating item {item_id} with quantity {quantity}")
        print("Updated Basket:", request.session['basket'])
        
        if item_id in basket:
            item = basket[item_id]
            item['quantity'] = quantity
            item['subtotal'] = quantity * Decimal(item['price'])
            basket[item_id] = item
            request.session.modified = True
        else:
            pass
        
        return JsonResponse({'success': 'Quantity updated successfully'})


class ClearBasketView(View):
    def post(self, request, *args, **kwargs):
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
        return HttpResponseRedirect(reverse('view_basket'))
