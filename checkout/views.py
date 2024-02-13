from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import View
from django.conf import settings

import stripe

from .models import Order, OrderLineItem
from edible_products.models import EdibleProduct
from basket.contexts import basket_contents
from .forms import OrderForm
from django.http import HttpResponseBadRequest

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        basket = basket_contents(request)
        if not basket['basket_items']: 
            messages.error(request, "There's nothing in your basket at the moment")
            return redirect(reverse('product_list'))

        order_form = OrderForm()
        current_basket = basket
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'basket_items': current_basket['basket_items'],
            'total': total,
            'grand_total': current_basket['grand_total'],
        }

        return render(request, 'checkout/checkout.html', context)

    def post(self, request, *args, **kwargs):
        basket = basket_contents(request)['basket_items']

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            for item in basket: 
                product = get_object_or_404(EdibleProduct, id=item['item_id'])
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    weight=item['weight'],
                )
                order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
            return redirect(reverse('checkout'))

        # Handle cases where the form is not valid; possibly return HTTP 400
        return HttpResponseBadRequest("Invalid form submission.")


class CheckoutSuccessView(View):
    def get(self, request, order_number, *arg, **kwargs):
        """
        Handle successful checkouts
        """
        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)
        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        if 'basket' in request.session:
            del request.session['basket']
        basket_items = order.orderlineitem_set.all()

        context = {
            'order': order,
            'basket_items': basket_items,
            'delivery': order.delivery_cost,
            'grand_total': order.grand_total,
        }

        return render(request, 'checkout/checkout_success.html', context)
