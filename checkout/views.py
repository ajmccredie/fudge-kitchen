from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.views.decorators.http import require_POST
from django.core import serializers
from decimal import Decimal
from django.utils import timezone

import stripe
import json

from .models import Order, OrderLineItem
from core.models import CommonProduct
from edible_products.models import EdibleProduct
from merch.models import MerchProduct, TextOption
from profiles.models import SubscriptionProduct
from basket.contexts import basket_contents
from .forms import OrderForm
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.serializers import serialize
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        context = basket_contents(request)
        
        if not context['basket_items']:
            messages.error(request, "There's nothing in your basket at the moment.")
            return redirect(reverse('product_list'))

        if request.user.is_authenticated:
            profile = request.user.profile
            initial_data = {
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'town_or_city': profile.default_town_or_city,
                'postcode': profile.default_postcode,
                'country': profile.default_country,
                'county': profile.default_county,
            }
        else:
            initial_data = {}

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
            'client_secret': intent.client_secret,
            'on_checkout': True 
        })

        return render(request, 'checkout/checkout.html', context)
        
    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        basket = request.session.get('basket', {})
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user_profile = request.user.profile if request.user.is_authenticated else None
            order.stripe_pid = request.POST.get('client_secret').split('_secret')[0]
            order.original_basket = json.dumps(basket)
            order.save()

            self.handle_line_items(order, basket)

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
            return render(request, 'checkout/checkout.html', {'order_form': order_form})

    def handle_line_items(self, order, basket):
        for item_id, item_data in basket.items():
            common_product = get_object_or_404(CommonProduct, id=item_id)
            product_type = common_product.product_type

            if product_type == 'edible':
                product = get_object_or_404(EdibleProduct, id=common_product.product_id)
                for weight, quantity in item_data['details'].items():
                    price_per_unit = product.get_price_for_weight(weight)
                    lineitem_total = price_per_unit * quantity
                    OrderLineItem.objects.create(
                        order=order,
                        edible_product=product,
                        product_type='edible',
                        weight=weight,
                        quantity=quantity,
                        lineitem_total=lineitem_total
                    )
            elif product_type == 'merch':
                product = get_object_or_404(MerchProduct, id=common_product.product_id)
                for text_option_id, quantity in item_data['details'].items():
                    lineitem_total = product.price * quantity
                    selected_text = get_object_or_404(TextOption, id=text_option_id)
                    OrderLineItem.objects.create(
                        order=order,
                        merch_product=product,
                        product_type='merch',
                        quantity=quantity,
                        lineitem_total=lineitem_total,
                        selected_text=selected_text
                    )
            elif product_type == 'subscription':
                product = get_object_or_404(SubscriptionProduct, id=common_product.product_id)
                quantity = item_data
                price_per_unit = product.price
                lineitem_total = price_per_unit * quantity
                OrderLineItem.objects.create(
                    order=order,
                    subscription_product=product,
                    product_type='subscription',
                    quantity=quantity,
                    lineitem_total=lineitem_total
                )
                if order.user_profile:
                    order.user_profile.is_subscribed = True
                    order.user_profile.subscription_start_date = timezone.now()
                    order.user_profile.save()

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
