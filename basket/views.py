from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.http import HttpRequest

# Define the class-based view
class BasketView(View):
    def get(self, request, *args, **kwargs):
        """ A view that renders the bag contents page """
        return render(request, 'basket/basket.html')


class AddToBasketView(View):
    def post(self, request: HttpRequest, item_id: str):
        """ Add a quantity of the specified product to the shopping basket """
        
        quantity = int(request.POST.get('quantity'))
        weight = request.POST.get('weight', '400')  # Default weight to '400' if not specified
        redirect_url = request.POST.get('redirect_url', reverse('view_basket'))
        
        basket = request.session.get('basket', {})
        weight_key = str(weight)

        if item_id in basket:
            if weight_key in basket[item_id]['items_by_weight']:
                basket[item_id]['items_by_weight'][weight_key] += quantity
            else:
                basket[item_id]['items_by_weight'][weight_key] = quantity
        else:
            basket[item_id] = {'items_by_weight': {weight_key: quantity}}

        request.session['basket'] = basket
        request.session.modified = True

        return redirect(redirect_url)

