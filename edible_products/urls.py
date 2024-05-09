from django.urls import path
from .views import EdibleProductListView, EdibleProductDetailView, GetPriceView, PlantBasedListView, TraditionalListView

urlpatterns = [
    path('', EdibleProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', EdibleProductDetailView.as_view(), name='product_detail'),
    path('get-price/', GetPriceView.as_view(), name='get_price'),
    path('product_list_plant/', PlantBasedListView.as_view(), name='plant_based_products'),
    path('product_list_trad/', TraditionalListView.as_view(), name='traditional_products'),
]