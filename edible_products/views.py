from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from .models import EdibleProduct, ProductWeightPrice

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
        weight = request.GET.get('weight')
        product_id = request.GET.get('product_id')
        try:
            weight = int(weight) 
            product = EdibleProduct.objects.get(pk=product_id)
            weight_price_obj = ProductWeightPrice.objects.get(product=product, weight=weight)
            return JsonResponse({'price': str(weight_price_obj.price)})
        except (ValueError, EdibleProduct.DoesNotExist, ProductWeightPrice.DoesNotExist, InvalidOperation):
            return JsonResponse({'error': 'Invalid product ID or weight'}, status=400)