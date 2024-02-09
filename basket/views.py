from django.shortcuts import render, redirect
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
        redirect_url = request.POST.get('redirect_url', '/')
        basket = request.session.get('basket', {})

        if item_id in list(basket.keys()):
            basket[item_id] += quantity
        else:
            basket[item_id] = quantity

        request.session['basket'] = basket
        print(request.POST)
        return redirect(redirect_url)
