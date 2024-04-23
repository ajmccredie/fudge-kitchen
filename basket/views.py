from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
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
        return render(request, 'basket/basket.html', context)


class AddToBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        """Add a quantity of the specified product to the shopping basket."""
        quantity = int(request.POST.get('quantity'))
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

        if item_id in basket:
            basket[item_key]['quantity'] += quantity
            basket[item_key]['price'] = str(price) 
            print(basket[item_key])
        else:
            basket[item_key] = {'quantity': quantity, 'weight': weight, 'flavour': flavour, 'price': str(price)}

        request.session['basket'] = basket
        request.session.modified = True

        print("basket line 61 - ", basket)

        messages.success(request, f'Added "{product.flavour}" to your basket.')
        return redirect(redirect_url)


class ClearBasketView(View):
    def post(self, request, *args, **kwargs):
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
        class AdjustBasketView(View):
            def post(self, request, *args, **kwargs):
                item_id = str(kwargs['item_id'])
                quantity = int(request.POST.get('quantity'))
                flavour = request.POST.get('flavour')
                weight = int(request.POST.get('weight'))

                basket = request.session.get('basket', {})

                item_key = f"{item_id}-{flavour}-{weight}"

                if item_key in basket:
                    if quantity > 0:
                        basket[item_key]['quantity'] = quantity
                    else:
                        del basket[item_key]
                        if not basket:
                            del request.session['basket']
                    request.session.modified = True
        messages.success(request, 'Basket successfully emptied for you to reimagine the delicious things you want...')
        return HttpResponseRedirect(reverse('view_basket'))


class RemoveFromBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        flavour = request.POST.get('flavour')
        weight = request.POST.get('weight')

        basket = request.session.get('basket', {})

        item_key = f"{item_id}-{flavour}-{weight}"
        try:
            if item_key in basket:
                basket.pop(item_key)
                if not basket:  
                    del request.session['basket']
                request.session['basket'] = basket
            messages.success(request, f'Removed "{flavour} {item.weight}" from your basket.')
            return HttpResponseRedirect(reverse('view_basket'))
        except Exception as e:
            return HttpResponse(status=500)


class AdjustBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        quantity = int(request.POST.get('quantity'))
        flavour = request.POST.get('flavour') 
        weight = int(request.POST.get('weight')) 

        product = get_object_or_404(EdibleProduct, pk=item_id)
        basket = request.session.get('basket', {})

        item_key = f"{item_id}-{flavour}-{weight}"

        if item_key in basket:
            if quantity > 0:
                basket[item_key]['quantity'] = quantity
                messages.success(request, f'Updated "{flavour} {product.name}" quantity in your basket.')
            else:
                del basket[item_key]
                if not basket:
                    del request.session['basket']
                messages.success(request, f'Removed "{flavour} {product.name}" from your basket.')
            request.session.modified = True
        else:
            messages.error(request, 'Item not found in your basket.')

        return redirect(reverse('view_basket'))


class RemoveFromBasketView(View):
    def post(self, request, *args, **kwargs):
        item_id = str(kwargs['item_id'])
        flavour = request.POST.get('flavour')
        weight = request.POST.get('weight')

        product = get_object_or_404(EdibleProduct, pk=item_id)
        basket = request.session.get('basket', {})

        item_key = f"{item_id}-{flavour}-{weight}"

        if item_key in basket:
            del basket[item_key]
            if not basket:  
                del request.session['basket']
            request.session.modified = True
        messages.success(request, f'Removed "{flavour} {product.weight}" from your basket.')
        return HttpResponseRedirect(reverse('view_basket'))
