from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, ListView
from edible_products.models import EdibleProduct, ProductWeightPrice
from .forms import EdibleProductForm

# Create your views here.

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to require user to be staff."""
    def test_func(self):
        return self.request.user.is_staff


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EdibleProductListView(StaffRequiredMixin, ListView):
    model = EdibleProduct
    template_name = 'dashboard/edible_product_list.html'
    context_object_name = 'products'


class EdibleProductCreateView(StaffRequiredMixin, CreateView):
    model = EdibleProduct
    form_class = EdibleProductForm
    template_name = 'dashboard/product_form.html'
    # fields = ['flavour', 'details', 'ingredients', 'quantity', 'weight', 'price', 'image', 'gluten', 'crustaceans', 'eggs', 'fish', 'peanuts', 'soybeans', 'milk', 'nuts', 'celery', 'mustard', 'sesame_seeds', 'sulphur_dioxide_and_sulphites', 'lupin', 'molluscs']

    def get_success_url(self):
        return reverse('dashboard:edible_product_list')


class EdibleProductUpdateView(StaffRequiredMixin, UpdateView):
    model = EdibleProduct
    form_class = EdibleProductForm
    template_name = 'dashboard/product_form.html'
    # fields = ['flavour', 'details', 'ingredients', 'quantity', 'weight', 'price', 'image', 'gluten', 'crustaceans', 'eggs', 'fish', 'peanuts', 'soybeans', 'milk', 'nuts', 'celery', 'mustard', 'sesame_seeds', 'sulphur_dioxide_and_sulphites', 'lupin', 'molluscs']

    def get_success_url(self):
        return reverse('dashboard:edible_product_list')


class EdibleProductDeleteView(StaffRequiredMixin, DeleteView):
    model = EdibleProduct
    template_name = 'dashboard/product_confirm_delete.html'

    def get_success_url(self):
        # Redirect to the product list view after a successful delete
        return reverse('dashboard:edible_product_list')