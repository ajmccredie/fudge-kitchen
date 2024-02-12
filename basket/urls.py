from django.urls import path
from .views import BasketView, AddToBasketView, UpdateBasketView, ClearBasketView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='view_basket'),
    path('add/<item_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('basket/update/<int:item_id>/', UpdateBasketView.as_view(), name='update_basket'),
    path('basket/clear/', ClearBasketView.as_view(), name='clear_basket'),
]