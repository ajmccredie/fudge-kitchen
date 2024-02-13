from django.urls import path
from .views import CheckoutView, CheckoutSuccessView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/success/<order_number>/', CheckoutSuccessView.as_view(), name='checkout_success'),
]