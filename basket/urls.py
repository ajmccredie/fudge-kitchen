from django.urls import path
from .views import (
    BasketView, AddToBasketView, ClearBasketView,
    AdjustBasketView, RemoveFromBasketView
)

app_name = 'basket'

urlpatterns = [
    path('', BasketView.as_view(), name='view_basket'),
    path('add/<item_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('clear/', ClearBasketView.as_view(), name='clear_basket'),
    path(
        'adjust/<int:item_id>/',
        AdjustBasketView.as_view(),
        name='adjust_basket'
    ),
    path(
        'remove/<int:item_id>/',
        RemoveFromBasketView.as_view(),
        name='remove_from_basket'
    ),
]
