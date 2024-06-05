from django.urls import path
from .views import MerchProductListView, MerchProductDetailView

app_name = 'merch'

urlpatterns = [
    path('', MerchProductListView.as_view(), name='merch_product_list'),
    path(
        'product/<int:pk>/',
        MerchProductDetailView.as_view(),
        name='merch_product_detail'
        ),
]
