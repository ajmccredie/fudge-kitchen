from django.urls import path
from . import views
from .views import DashboardView, EdibleProductListView, EdibleProductCreateView, EdibleProductUpdateView, EdibleProductDeleteView, MerchProductListView, MerchProductCreateView, MerchProductUpdateView, MerchProductDeleteView, OrderListView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('products/', EdibleProductListView.as_view(), name='edible_product_list'),
    path('products/new/', EdibleProductCreateView.as_view(), name='edible_product_create'),
    path('products/edit/<int:pk>/', EdibleProductUpdateView.as_view(), name='edible_product_edit'),
    path('products/delete/<int:pk>/', EdibleProductDeleteView.as_view(), name='edible_product_delete'),
    path('merch/', MerchProductListView.as_view(), name='merch_product_list'),
    path('merch/new/', MerchProductCreateView.as_view(), name='merch_product_create'),
    path('merch/<int:pk>/edit/', MerchProductUpdateView.as_view(), name='merch_product_update'),
    path('merch/<int:pk>/delete/', MerchProductDeleteView.as_view(), name='merch_product_delete'),
    path('order_list', OrderListView.as_view(), name='order_list'),
]