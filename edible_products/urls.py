from django.urls import path
from .views import EdibleProductListView, EdibleProductDetailView

urlpatterns = [
    path('', EdibleProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', EdibleProductDetailView.as_view(), name='product_detail'),
]