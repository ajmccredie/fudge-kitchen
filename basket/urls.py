from django.urls import path
from .views import BasketView, AddToBasketView,  AddMerchToBasketView, ClearBasketView, AdjustBasketView, RemoveFromBasketView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('add/<item_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('add/merch/<int:item_id>/', AddMerchToBasketView.as_view(), name='add_merch_to_basket'),
    path('basket/clear/', ClearBasketView.as_view(), name='clear_basket'),
    path('basket/adjust/<int:item_id>/', AdjustBasketView.as_view(), name='adjust_basket'),
    path('basket/remove/<int:item_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
]