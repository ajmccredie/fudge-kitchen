from django.views.generic import DetailView, ListView
from .models import MerchProduct


class MerchProductListView(ListView):
    model = MerchProduct
    template_name = 'merch/merch_product_list.html'
    context_object_name = 'merch_products'

    def get_queryset(self):
        """Override the default queryset to filter by category
        if it is provided in the URL."""
        queryset = super().get_queryset()
        product_type = self.request.GET.get('type')
        if product_type:
            queryset = queryset.filter(type__icontains=product_type)
        return queryset


class MerchProductDetailView(DetailView):
    model = MerchProduct
    template_name = 'merch/merch_product_detail.html'
    context_object_name = 'merch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colours'] = self.object.colours.all()
        context['text_options'] = self.object.text_option.all()
        return context
