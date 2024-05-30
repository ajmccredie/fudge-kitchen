from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from decimal import InvalidOperation
from .models import EdibleProduct, ProductWeightPrice
from .forms import AllergenFilterForm


class EdibleProductListView(ListView):
    model = EdibleProduct
    template_name = 'edible_products/product_list.html'
    context_object_name = 'edible_products'

    def get_queryset(self):
        queryset = super().get_queryset()
        allergens_selected = self.request.GET.getlist('allergens')

        if allergens_selected:
            for allergen in allergens_selected:
                queryset = queryset.exclude(**{allergen: True})

        print("Number of products found:", queryset.count())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edible_products = self.get_queryset()
        for product in edible_products:
            product.price_400g = product.get_price_for_weight(400)
        context['edible_products'] = edible_products
        context['allergen_form'] = AllergenFilterForm(self.request.GET)
        return context


class PlantBasedListView(EdibleProductListView):
    template_name = 'edible_products/product_list_plant.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter only plant-based products
        queryset = queryset.filter(plant_based=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Plant Based Deliciousness'
        return context


class TraditionalListView(EdibleProductListView):
    template_name = 'edible_products/product_list_trad.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter out plant-based products
        queryset = queryset.filter(plant_based=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Traditional Delights'
        return context


class EdibleProductDetailView(DetailView):
    model = EdibleProduct
    context_object_name = 'edible_product'
    template_name = 'edible_products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['price_400g'] = product.get_price_for_weight(400)
        return context


class GetPriceView(View):
    def get(self, request, *args, **kwargs):
        weight = request.GET.get('weight')
        product_id = request.GET.get('product_id')
        try:
            weight = int(weight)
            product = EdibleProduct.objects.get(pk=product_id)
            weight_price_obj = ProductWeightPrice.objects.get(
                product=product, weight=weight
            )
            return JsonResponse({'price': str(weight_price_obj.price)})
        except (
            ValueError,
            EdibleProduct.DoesNotExist,
            ProductWeightPrice.DoesNotExist,
            InvalidOperation,
        ):
            return JsonResponse(
                {'error': 'Invalid product ID or weight'}, status=400
            )
