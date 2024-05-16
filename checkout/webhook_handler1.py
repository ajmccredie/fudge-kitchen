import json
import time
import stripe
from django.http import HttpResponse
from django.conf import settings
from .models import Order, OrderLineItem
from edible_products.models import EdibleProduct

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)
            

    def handle_payment_intent_succeeded(self, event):
        intent = event['data']['object']
        order_reference = intent['metadata'].get('order_reference')

        try:
            order = Order.objects.get(order_number=order_reference)
            order.status = 'completed'
            order.save()
            send_order_confirmation_email(order) 
            messages.success(self.request, f"Thank you! Your payment has been successfully processed. Order Number: {order.order_number}")
            return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS: Order processed successfully', status=200)
        except Order.DoesNotExist:
            logger.error(f"Order not found in database: {order_reference}")
            return HttpResponse(content='Order not found.', status=404)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
