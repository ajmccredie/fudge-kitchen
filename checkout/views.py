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

@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret')
        if client_secret:
            pid = client_secret.split('_secret')[0]
            print("Cache pid: ", pid)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # print('basket', json.dumps(request.session.get('basket', {})))
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

# @require_POST
# def cache_checkout_data(request):
#     try:
#         client_secret = request.POST.get('client_secret')
#         if client_secret:
#             pid = client_secret.split('_secret')[0]
#             stripe.api_key = settings.STRIPE_SECRET_KEY

#             # Get the basket data
#             basket_data = request.session.get('basket', {})
#             # Get the first line of basket metadata
#             basket_first_line = next(iter(basket_data.values()), '')

#             # Clean the first line of basket metadata
#             cleaned_basket_first_line = basket_first_line.split('-')[0]

#             # Modify the PaymentIntent metadata with the cleaned basket data
#             stripe.PaymentIntent.modify(pid, metadata={
#                 'basket': json.dumps({0: cleaned_basket_first_line}),
#                 'save_info': request.POST.get('save_info'),
#             })
#             return HttpResponse(status=200)
#         else:
#             raise ValueError('Client secret not found in the request.')
#     except Exception as e:
#         messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
#         return HttpResponse(content=e, status=400)



class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        basket = basket_contents(request)
        if not basket['basket_items']:
            messages.error(request, "There's nothing in your basket at the moment.")
            return redirect(reverse('product_list'))

        # Calculate total from basket items
        total = sum(item['price'] * item['quantity'] for item in basket['basket_items'])

        # Handling delivery costs
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_subscriber:
            delivery = 0  # Free delivery for subscribers
        else:
            delivery = 3  # Standard delivery fee

        grand_total = total + delivery

        # Stripe total calculation for payment intent
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        context = {
            'order_form': OrderForm(),
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'basket_items': basket['basket_items'],
            'total': total, 
            'delivery': delivery,
            'grand_total': grand_total,
        }

        return render(request, 'checkout/checkout.html', context)

    def post(self, request, *args, **kwargs):
        basket_items = basket_contents(request)['basket_items']

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
            print("Order is valid")
            pid = request.POST.get('client_secret')
            if pid:
                pid = pid.split('_secret')[0]
                print("The valid pid is:", pid)
                order.stripe_pid = pid
                
                # Serializing each basket item
                serializable_basket = json.dumps([{
                    'id': item['product'].id,
                    'name': item['product'].flavour,
                    'quantity': item['quantity'],
                    'price': str(item['product'].price),
                    'weight': item['weight']
                } for item in basket_items])

                order.original_basket = serializable_basket
                order.save()

                for item in basket_items:
                    product = get_object_or_404(EdibleProduct, id=item['product'].id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        weight=item['weight'],
                        lineitem_total=product.price * item['quantity']
                    )
                    order_line_item.save()
                
                order.update_total()

                request.session['save_info'] = 'save-info' in request.POST
            
                if order.order_number:
                    return redirect(reverse('checkout_success', args=[order.order_number]))
                else:
                    messages.error(request, 'Order number is missing.')
                    return redirect(reverse('checkout'))
            else:
                messages.error(request, 'Client secret is missing in the request.')
                return redirect(reverse('checkout'))
        else:
            messages.error(request, 'There was an error with your form submission.')
            return redirect(reverse('checkout'))

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
