from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from .models import EdibleProduct, ProductWeightPrice, Allergen

class EdibleProductListView(ListView):
    model = EdibleProduct
    context_object_name = 'edible_products'
    template_name = 'edible_products/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        allergen_ids = self.request.GET.getlist('allergen[]')
        print(allergen_ids)
        query = self.request.GET.get('q')

        if allergen_ids:
            allergen_filter = Q()
            for allergen_id in allergen_ids:
                allergen_filter |= Q(allergens__id=allergen_id)
            queryset = queryset.exclude(allergen_filter)

        if query:
            queryset = queryset.filter(name__icontains=query) 

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allergens'] = Allergen.objects.all()  # Pass allergens to the template
        return context

class EdibleProductDetailView(DetailView):
    model = EdibleProduct
    context_object_name = 'edible_product'
    template_name = 'edible_products/product_detail.html'

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

