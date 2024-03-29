from django.urls import path
from .views import CheckoutView, CheckoutSuccessView, cache_checkout_data
from .webhooks import webhook

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<order_number>/', CheckoutSuccessView.as_view(), name='checkout_success'),
    path('wh/', webhook, name='webhook'),
    path('cache_checkout_data/', cache_checkout_data, name='cache_checkout_data'),
]