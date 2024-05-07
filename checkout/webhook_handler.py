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

    # def handle_payment_intent_succeeded(self, event):
    #     """
    #     Handle the payment_intent.succeeded webhook from Stripe
    #     """
    #     intent = event['data']['object']
    #     pid = intent['id']
    #     basket = json.loads(intent['metadata']['basket'])

    #     # Check if charges data exists and has at least one charge object
    #     if 'charges' in intent and intent['charges']['data']:
    #         charge = intent['charges']['data'][0]  # Get the first charge in the list
    #         charge_id = charge['id']

    #         try:
    #             stripe_charge = stripe.Charge.retrieve(
    #                 charge_id,
    #                 api_key=settings.STRIPE_SECRET_KEY
    #             )
    #         except Exception as e:
    #             print(f"Error retrieving Stripe Charge: {e}")
    #             return HttpResponse(
    #                 content=f'Error in webhook: {e}',
    #                 status=500)

    #         billing_details = stripe_charge.billing_details
    #         shipping_details = intent['shipping']
    #         grand_total = round(stripe_charge.amount / 100, 2)

    #         # Clean up the shipping details
    #         for field, value in shipping_details['address'].items():
    #             if value == "":
    #                 shipping_details['address'][field] = None

    #         order_exists = False
    #         attempt = 1
    #         while attempt <= 5:
    #             try:
    #                 order = Order.objects.get(
    #                     full_name__iexact=shipping_details['name'],
    #                     email__iexact=billing_details['email'],
    #                     phone_number__iexact=shipping_details['phone'],
    #                     country__iexact=shipping_details['address']['country'],
    #                     postcode__iexact=shipping_details['address']['postal_code'],
    #                     town_or_city__iexact=shipping_details['address']['city'],
    #                     street_address1__iexact=shipping_details['address']['line1'],
    #                     street_address2__iexact=shipping_details['address']['line2'],
    #                     county__iexact=shipping_details['address']['state'],
    #                     grand_total=grand_total,
    #                     original_basket=json.dumps(basket),
    #                     stripe_pid=pid,
    #                 )
    #                 order_exists = True
    #                 break
    #             except Order.DoesNotExist:
    #                 attempt += 1
    #                 time.sleep(1)

    #         if order_exists:
    #             return HttpResponse(
    #                 content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
    #                 status=200)
    #         else:
    #             # Create the order if not found after retries
    #             order = None
    #             try:
    #                 order = Order.objects.create(
    #                     full_name=shipping_details['name'],
    #                     email=billing_details['email'],
    #                     phone_number=shipping_details['phone'],
    #                     country=shipping_details['address']['country'],
    #                     postcode=shipping_details['address']['postal_code'],
    #                     town_or_city=shipping_details['address']['city'],
    #                     street_address1=shipping_details['address']['line1'],
    #                     street_address2=shipping_details['address']['line2'],
    #                     county=shipping_details['address']['state'],
    #                     original_basket=json.dumps(basket),
    #                     stripe_pid=pid,
    #                 )
    #                 for item_id, item_details in basket.items():
    #                     product = EdibleProduct.objects.get(id=int(item_id))
    #                     OrderLineItem.objects.create(
    #                         order=order,
    #                         product=product,
    #                         quantity=item_details['quantity']
    #                     )
    #             except Exception as e:
    #                 if order:
    #                     order.delete()
    #                 return HttpResponse(
    #                     content=f'Webhook received: {event["type"]} | ERROR: {e}',
    #                     status=500)
    #         return HttpResponse(
    #             content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
    #             status=200)
    #     else:
    #         # Handle the case where no charges are found
    #         print("No charges found in the PaymentIntent.")
    #         return HttpResponse(
    #             content='Error in webhook: No charges found',
    #             status=400)

    def handle_payment_intent_succeeded(self, event):
        intent = event['data']['object']
        order_reference = intent['metadata']['order_reference']  # This is your order_number from the metadata

        try:
            order = Order.objects.get(order_number=order_reference)
            # Here you would update order status to something like 'completed'
            order.status = 'completed'
            order.save()
            # You might want to trigger a signal here or send a confirmation email as well
            send_order_confirmation_email(order)  # Assuming this function exists
            messages.success(self.request, f"Thank you! Your payment has been successfully processed. Order Number: {order.order_number}")
            return HttpResponse(content=f'Webhook received: {event["type"]} | SUCCESS: Order processed successfully', status=200)
        except Order.DoesNotExist:
            # Log this error, possibly alert admins
            logger.error(f"Order not found in database: {order_reference}")
            return HttpResponse(content='Order not found.', status=404)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
