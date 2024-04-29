from django.urls import path
from . import views
from .views import DashboardView, EdibleProductListView, EdibleProductCreateView, EdibleProductUpdateView, EdibleProductDeleteView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('products/', EdibleProductListView.as_view(), name='edible_product_list'),
    path('products/new/', EdibleProductCreateView.as_view(), name='edible_product_create'),
    path('products/edit/<int:pk>/', EdibleProductUpdateView.as_view(), name='edible_product_edit'),
    path('products/delete/<int:pk>/', EdibleProductDeleteView.as_view(), name='edible_product_delete'),
]