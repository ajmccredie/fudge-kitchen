from django.urls import path
from .views import EdibleProductListView, EdibleProductDetailView, GetPriceView

urlpatterns = [
    path('', EdibleProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', EdibleProductDetailView.as_view(), name='product_detail'),
    path('get-price/', GetPriceView.as_view(), name='get_price'),
]