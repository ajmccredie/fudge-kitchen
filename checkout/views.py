from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core import serializers

import stripe
import json

from .models import Order, OrderLineItem
from edible_products.models import EdibleProduct
from basket.contexts import basket_contents
from .forms import OrderForm
from django.http import HttpResponseBadRequest
from django.core.serializers import serialize
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret')
        if client_secret:
            pid = client_secret.split('_secret')[0]
            print("Cache pid: ", pid)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            print('basket in cache checkout data', json.dumps(request.session.get('basket', {})))
            stripe.PaymentIntent.modify(pid, metadata={
                'basket': json.dumps(request.session.get('basket', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)
        else:
            raise ValueError('Client secret not found in the request.')
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        context = basket_contents(request)  # Fetch the basket context

        if not context['basket_items']:
            messages.error(request, "There's nothing in your basket at the moment.")
            return redirect(reverse('product_list'))

        # Setup initial form data
        initial_data = {'email': request.user.email} if request.user.is_authenticated else {}
        order_form = OrderForm(initial=initial_data)

        # Create Stripe PaymentIntent
        stripe.api_key = settings.STRIPE_SECRET_KEY
        total = int(context['grand_total'] * 100)
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={'basket': json.dumps(request.session.get('basket', {}))}
        )

        context = {
            'order_form': order_form,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret
        }

        return render(request, 'checkout/checkout.html', context)



    def post(self, request, *args, **kwargs):
        context = basket_contents(request)  # Fetch the basket context again
        basket_items = context['basket_items']

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
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid

            # Prepare a serializable version of basket items
            serializable_basket = json.dumps([{
                'item_id': item['product'].id,
                'name': item['product'].flavour,
                'quantity': item['quantity'],
                'weight': item['weight'],
                'price': str(item['price']),
                'subtotal': str(item['subtotal']),
            } for item in basket_items], default=str)

            order.original_basket = serializable_basket
            order.save()

            # Create order line items
            for item in basket_items:
                product = item['product']
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    weight=item['weight'],
                    lineitem_total=item['price'] * item['quantity']
                )

            order.update_total()  # Update the order total, which may trigger other business logic

            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, "There was an error with your form submission.")
            return render(request, 'checkout/checkout.html', {'order_form': order_form, **context})
            


class CheckoutSuccessView(View):
    def get(self, request, order_number, *arg, **kwargs):
        """
        Handle successful checkouts
        """
        save_info = request.session.get('save_info')
        order = get_object_or_404(Order, order_number=order_number)
        # toast message 
        messages.success(request, f'Order successfully processed! \
            Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

        # email confirmation
        subject = "Roo's Fudge Kitchen Order Confirmation - Your Latest Order"
        message = render_to_string('emails/order_confirmation.html', {'order': order})
        email = EmailMessage(subject, message, to=[order.email])
        email.content_subtype = 'html'  # (set to send the html contents
        email.send()

        if 'basket' in request.session:
            del request.session['basket']

        basket_items = order.lineitems.all()

        context = {
            'order': order,
            'basket_items': basket_items,
            'delivery': order.delivery_cost,
            'total': order.order_total,
            'grand_total': order.grand_total,
            'on_checkout_success': True,
        }

        return render(request, 'checkout/checkout_success.html', context)
