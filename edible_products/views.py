from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from .models import EdibleProduct

class EdibleProductListView(ListView):
    model = EdibleProduct
    context_object_name = 'edible_products'
    template_name = 'edible_products/product_list.html'


class EdibleProductDetailView(DetailView):
    model = EdibleProduct
    context_object_name = 'edible_product'
    template_name = 'edible_products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class GetPriceView(View):
    def get(self, request, *args, **kwargs):
        weight = kwargs.get('weight')
        price_lookup = {100: 3.50, 400: 7.00, 800: 11.00}
        price = price_lookup.get(weight, "Error: Invalid weight")
        
        # Return price as JSON response
        if price != "Error: Invalid weight":
            return JsonResponse({'price': price})
        else:
            return JsonResponse({'error': price}, status=400)