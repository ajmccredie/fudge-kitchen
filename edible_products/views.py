from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import EdibleProduct

class EdibleProductListView(ListView):
    model = EdibleProduct
    context_object_name = 'edible_products'
    template_name = 'edible_products/product_list.html'
 #   queryset = EdibleProduct.objects.all().select_related('Allergens')

class EdibleProductDetailView(DetailView):
    model = EdibleProduct
    context_object_name = 'edible_product'
    template_name = 'edible_products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context