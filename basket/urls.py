from django.urls import path
from .views import BasketView, AddToBasketView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('add/<item_id>/', AddToBasketView.as_view(), name='add_to_basket'),
]