from django.urls import path
from .views import BasketView, AddToBasketView, ClearBasketView, AdjustBasketView, RemoveFromBasketView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('add/<item_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('basket/clear/', ClearBasketView.as_view(), name='clear_basket'),
    path('basket/adjust/<str:item_id>/', AdjustBasketView.as_view(), name='adjust_basket'),
    path('basket/remove/<str:item_key>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
]