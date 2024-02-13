from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import View
from django.conf import settings

import stripe

from basket.contexts import basket_contents
from .forms import OrderForm

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        basket_items = basket_contents(request)
        if not basket_items:
            messages.error(request, "There's nothing in your basket at the moment")
            return redirect(reverse('product_list'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(intent)

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': 'pk_test_51OhByXCnqJdd7RmYyBtN9FKq1Uol9CDaIt4vXEpLTTGF77af9OLMOpurtcrquUONaH2JIrm9ZOJZkDvB8UejGomj00tA7MwXmi',
            'client_secret': 'test client secret',
        }

        return render(request, template, context)
