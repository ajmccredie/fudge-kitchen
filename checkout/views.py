from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core import serializers
from decimal import Decimal

import stripe
import json

from .models import Order, OrderLineItem
from edible_products.models import EdibleProduct
from merch.models import MerchProduct, TextOption
from basket.contexts import basket_contents
from .forms import OrderForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.serializers import serialize
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# @require_POST
# def cache_checkout_data(request):
#     try:
#         client_secret = request.POST.get('client_secret')
#         print("Client secret:")
#         print(client_secret)
#         order_number = request.POST.get('order_number')
#         print("Order number:")
#         print(order_number)
#         if not client_secret or not order_number:
#             print("Missing data: client_secret or order_number is None.")
#             return JsonResponse({'error': 'Missing data!'}, status=400)

#         pid = client_secret.split('_secret')[0]
#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         stripe.PaymentIntent.modify(
#             pid,
#             metadata={
#                 'order_number': order_number,
#                 'username': request.user.username if request.user.is_authenticated else 'Guest'
#             }
#         )
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
#         return HttpResponse(content=e, status=400)

@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret')
        order_number = request.POST.get('order_number')
        if client_secret:
            pid = client_secret.split('_secret')[0]
            print("Cache pid: ", pid)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            print('basket in cache checkout data', json.dumps(request.session.get('basket', {})))
            stripe.PaymentIntent.modify(pid, metadata={
                'basket': json.dumps(request.session.get('basket', {})),
                'order_number': order_number, 
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)
        else:
            raise ValueError('Client secret not found in the request.')
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# class CheckoutView(View):
    # def get(self, request, *args, **kwargs):
    #     context = basket_contents(request)  # Fetch the basket context
    #     print(context['basket_items'])

    #     if not context['basket_items']:
    #         messages.error(request, "There's nothing in your basket at the moment.")
    #         return redirect(reverse('product_list'))

    #     # Setup initial form data
    #     initial_data = {'email': request.user.email} if request.user.is_authenticated else {}
    #     order_form = OrderForm(initial=initial_data)

    #     # Create Stripe PaymentIntent
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
    #     total = int(context['grand_total'] * 100)
    #     intent = stripe.PaymentIntent.create(
    #         amount=total,
    #         currency='gbp',
    #         metadata={'basket': json.dumps(request.session.get('basket', {}))}
    #     )

    #     context = {
    #         'order_form': order_form,
    #         'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    #         'client_secret': intent.client_secret
    #     }

    #     return render(request, 'checkout/checkout.html', context)

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        context = basket_contents(request)
        
        if not context['basket_items']:
            messages.error(request, "There's nothing in your basket at the moment.")
            return redirect(reverse('product_list'))

        initial_data = {
            'email': request.user.email,
        } if request.user.is_authenticated else {}

        order_form = OrderForm(initial=initial_data)

        # Create Stripe PaymentIntent
        stripe.api_key = settings.STRIPE_SECRET_KEY
        total = int(context['grand_total'] * 100)
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={'user_id': request.user.id if request.user.is_authenticated else 'guest'}
        )

        context.update({
            'order_form': order_form,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret
        })

        return render(request, 'checkout/checkout.html', context)

    # def post(self, request, *args, **kwargs):
    #     context = basket_contents(request)
    #     form_data = {
    #         'full_name': request.POST['full_name'],
    #         'email': request.POST['email'],
    #         'phone_number': request.POST['phone_number'],
    #         'country': request.POST['country'],
    #         'postcode': request.POST['postcode'],
    #         'town_or_city': request.POST['town_or_city'],
    #         'street_address1': request.POST['street_address1'],
    #         'street_address2': request.POST['street_address2'],
    #         'county': request.POST['county'],
    #     }

    #     order_form = OrderForm(form_data)
    #     if order_form.is_valid():
    #         order = order_form.save(commit=False)
    #         pid = request.POST.get('client_secret').split('_secret')[0]
    #         order.stripe_pid = pid
    #         order.save()

    #         # Handle different types of products
    #         for item_key, item_data in context['basket_items'].items():
    #             product = get_object_or_404(EdibleProduct if 'edible' in item_key else MerchProduct, pk=item_data['product_id'])
    #             quantity = item_data['quantity']
    #             price = Decimal(item_data['price'])

    #             OrderLineItem.objects.create(
    #                 order=order,
    #                 product=product,
    #                 quantity=quantity,
    #                 weight=item_data.get('weight', None),  # Only for edible products
    #                 lineitem_total=price * quantity
    #             )

    #         order.update_total()  # Update the order total
    #         return redirect(reverse('checkout_success', args=[order.order_number]))
    #     else:
    #         messages.error(request, "There was an error with your form submission.")
    #         return render(request, 'checkout/checkout.html', {'order_form': order_form, **context})
    
    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        basket = request.session.get('basket', {})
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user_profile = request.user.profile if request.user.is_authenticated else None
            print(order.user_profile)
            order.stripe_pid = request.POST.get('client_secret').split('_secret')[0]
            order.original_basket = json.dumps(basket)
            order.save()

            self.handle_line_items(order, request.session.get('basket', {}))

            # Setup Stripe payment intent with metadata
            stripe.api_key = settings.STRIPE_SECRET_KEY
            total = int(order.grand_total * 100)
            intent = stripe.PaymentIntent.create(
                amount=total,
                currency='gbp',
                metadata={'order_reference': order.order_number}
            )

            if 'basket' in request.session:
                del request.session['basket']

            return redirect('checkout_success', order.order_number)
        else:
            messages.error(request, "There was an error with your form. Please double-check your information.")
            return render(request, self.template_name, {'order_form': order_form})

    def handle_line_items(self, order, basket):
        for item_id, item_details in basket.items():
            quantity = Decimal(item_details['quantity'])
      
            if item_details['product_type'] == 'edible':
                edible_product = get_object_or_404(EdibleProduct, pk=int(item_details['product_id']))
                price_per_unit = edible_product.get_price_for_weight(item_details['weight'])
                lineitem_total = price_per_unit * quantity
            
                OrderLineItem.objects.create(
                    order=order,
                    edible_product=edible_product,
                    product_type='edible',
                    weight=item_details['weight'],
                    quantity=quantity,
                    lineitem_total=lineitem_total
                )

            elif item_details['product_type'] == 'merch':
                merch_product = get_object_or_404(MerchProduct, pk=int(item_details['product_id']))
                if 'text_option_id' not in item_details:
                    raise ValueError("Selected text ID missing for merch product")
                selected_text = get_object_or_404(TextOption, pk=int(item_details['text_option_id'])) 
                lineitem_total = merch_product.price * quantity
                
                OrderLineItem.objects.create(
                    order=order,
                    merch_product=merch_product,
                    product_type='merch',
                    quantity=quantity,
                    selected_text=selected_text,
                    lineitem_total=lineitem_total
                )
        order.update_total()
            

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
        # email.send()

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
