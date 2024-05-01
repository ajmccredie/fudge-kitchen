from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import MerchProduct

# Create your views here.

from django.views.generic import DetailView, ListView
from .models import MerchProduct

class MerchProductListView(ListView):
    model = MerchProduct
    template_name = 'merch/merch_product_list.html'

class MerchProductDetailView(DetailView):
    model = MerchProduct
    template_name = 'merch/merch_product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context