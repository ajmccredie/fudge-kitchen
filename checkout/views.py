from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import View

from .forms import OrderForm

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your basket at the moment")
            return redirect(reverse('product_list'))

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': 'pk_test_51OhByXCnqJdd7RmYyBtN9FKq1Uol9CDaIt4vXEpLTTGF77af9OLMOpurtcrquUONaH2JIrm9ZOJZkDvB8UejGomj00tA7MwXmi',
            'client_secret': 'test client secret',
        }

        return render(request, template, context)
