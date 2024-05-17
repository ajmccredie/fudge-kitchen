from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, ListView, DetailView
from edible_products.models import EdibleProduct, ProductWeightPrice, Allergen
from merch.models import MerchProduct
from checkout.models import Order, OrderLineItem
from home.models import Inquiry
from .forms import EdibleProductForm, MerchProductForm, OrderForm, OrderLineItemForm

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product created successfully!')
        return response

    def get_success_url(self):
        return reverse('dashboard:edible_product_list')


class EdibleProductUpdateView(StaffRequiredMixin, UpdateView):
    model = EdibleProduct
    form_class = EdibleProductForm
    template_name = 'dashboard/product_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Product updated successfully!')
        return response

    def get_success_url(self):
        return reverse('dashboard:edible_product_list')


class EdibleProductDeleteView(StaffRequiredMixin, DeleteView):
    model = EdibleProduct
    template_name = 'dashboard/product_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Product deleted successfully!')
        return response

    def get_success_url(self):
        # Redirect to the product list view after a successful delete
        return reverse('dashboard:edible_product_list')


class MerchProductListView(StaffRequiredMixin, ListView):
    model = MerchProduct
    template_name = 'dashboard/merch_product_list.html'
    context_object_name = 'merch_products'

class MerchProductCreateView(StaffRequiredMixin, CreateView):
    model = MerchProduct
    form_class = MerchProductForm
    template_name = 'dashboard/merch_product_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ColourVariationFormSet(self.request.POST, self.request.FILES)
        else:
            data['formset'] = ColourVariationFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Merch product created successfully!')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('dashboard:merch_product_list')

class MerchProductUpdateView(StaffRequiredMixin, UpdateView):
    model = MerchProduct
    form_class = MerchProductForm
    template_name = 'dashboard/merch_product_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ColourVariationFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['formset'] = ColourVariationFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Merch product updated successfully!')
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('dashboard:merch_product_list')

class MerchProductDeleteView(StaffRequiredMixin, DeleteView):
    model = MerchProduct
    template_name = 'dashboard/merch_product_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Merch product deleted successfully!')
        return response

    def get_success_url(self):
        return reverse('dashboard:merch_product_list')


class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'dashboard/order_list.html'
    context_object_name = 'object_list'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by dispatch status
        if self.request.GET.get('filter_dispatch'):
            queryset = queryset.filter(dispatched=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_dispatch'] = self.request.GET.get('filter_dispatch', '')
        context['filter_type'] = self.request.GET.get('filter_type', '')
        return context

class OrderDetailView(StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'

def mark_order_dispatched(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.dispatched = True
    order.save()
    return redirect('dashboard:order_list')

def mark_item_made(request, item_id):
    item = get_object_or_404(OrderLineItem, id=item_id)
    item.made = True
    item.save()
    return redirect('dashboard:order_details', pk=item.order.id)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order has been successfully deleted.")
    return redirect('dashboard:order_list')


class InquiryListView(StaffRequiredMixin, View):
    template_name = 'dashboard/inquiries_list.html'

    def get(self, request, *args, **kwargs):
        inquiries = Inquiry.objects.all().order_by('-created_at')
        context = {
            'inquiries': inquiries,
        }
        return render(request, self.template_name, context)

class InquiryDetailView(StaffRequiredMixin, View):
    template_name = 'dashboard/inquiries_detail.html'

    def get(self, request, pk, *args, **kwargs):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        if inquiry.is_new:
            inquiry.is_new = False
            inquiry.save()
        context = {
            'inquiry': inquiry,
        }
        return render(request, self.template_name, context)

class MarkInquiryDealtWithView(StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        inquiry = get_object_or_404(Inquiry, pk=pk)
        inquiry.is_dealt_with = True
        inquiry.save()
        messages.success(request, 'Inquiry marked as dealt with.')
        return redirect('dashboard:inquiries_detail', pk=pk)