from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, UpdateView, DeleteView, TemplateView,
    ListView, DetailView
)
from profiles.models import Profile, SubscriptionProduct
from profiles.forms import ProfileForm
from core.models import Product
from edible_products.models import EdibleProduct
from merch.models import MerchProduct
from checkout.models import Order, OrderLineItem
from home.models import Inquiry
from .forms import (
    EdibleProductForm, MerchProductForm, ColourVariationFormSet,
    TextOptionFormSet, SubscriptionProductForm
)


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
        if not form.is_valid():
            messages.error(self.request, 'Please correct the errors below.')
            return self.form_invalid(form)

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
        if not form.is_valid():
            messages.error(self.request, 'Please correct the errors below.')
            return self.form_invalid(form)

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
            data['colour_formset'] = ColourVariationFormSet(
                self.request.POST, self.request.FILES
            )
            data['text_option_formset'] = TextOptionFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data['colour_formset'] = ColourVariationFormSet()
            data['text_option_formset'] = TextOptionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        colour_formset = context['colour_formset']
        text_option_formset = context['text_option_formset']
        if (
            form.is_valid()
            and colour_formset.is_valid()
            and text_option_formset.is_valid()
        ):
            self.object = form.save()
            colour_formset.instance = self.object
            colour_formset.save()
            text_option_formset.instance = self.object
            text_option_formset.save()
            messages.success(
                self.request, 'Merch product created successfully!'
            )
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error with your submission. '
            'Please check the form and try again.'
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('dashboard:merch_product_list')


class MerchProductUpdateView(StaffRequiredMixin, UpdateView):
    model = MerchProduct
    form_class = MerchProductForm
    template_name = 'dashboard/merch_product_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['colour_formset'] = ColourVariationFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
            data['text_option_formset'] = TextOptionFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data['colour_formset'] = ColourVariationFormSet(
                instance=self.object
            )
            data['text_option_formset'] = TextOptionFormSet(
                instance=self.object
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        colour_formset = context['colour_formset']
        text_option_formset = context['text_option_formset']
        if (
            form.is_valid()
            and colour_formset.is_valid()
            and text_option_formset.is_valid()
        ):
            self.object = form.save()
            colour_formset.instance = self.object
            colour_formset.save()
            text_option_formset.instance = self.object
            text_option_formset.save()
            messages.success(
                self.request, 'Merch product updated successfully!'
            )
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'There was an error with your submission. '
            'Please check the form and try again.'
        )
        return super().form_invalid(form)

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
        if self.request.GET.get('filter_dispatch'):
            queryset = queryset.filter(dispatched=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_dispatch'] = self.request.GET.get(
            'filter_dispatch', ''
        )
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


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product_list.html', context)


class ClearBasketCacheView(View):
    def post(self, request, *args, **kwargs):
        if 'basket' in request.session:
            del request.session['basket']
            request.session.modified = True
        return redirect('/')


class SubscriptionManagementView(StaffRequiredMixin, View):
    template_name = 'dashboard/subscription_management.html'

    def get(self, request, *args, **kwargs):
        subscriptions = Profile.objects.filter(is_subscribed=True)
        subscription_products = SubscriptionProduct.objects.all()
        allergen_fields = ProfileForm.ALLERGEN_FIELDS

        for profile in subscriptions:
            allergen_info = {
                field: getattr(profile, field) for field, _ in allergen_fields
            }
            profile.user.allergen_display = ", ".join([
                label for field, label in allergen_fields
                if allergen_info.get(field)
            ])
            profile.user.dietary_preference_display = (
                profile.get_dietary_preference_display()
            )

            if not profile.user.allergen_display:
                profile.user.allergen_display = "None selected"

            if profile.user.dietary_preference_display == "None":
                profile.user.dietary_preference_display = "None selected"

        context = {
            'subscriptions': subscriptions,
            'subscription_products': subscription_products,
            'allergen_fields': allergen_fields,
        }

        return render(request, self.template_name, context)


class SubscriptionProductListView(StaffRequiredMixin, ListView):
    model = SubscriptionProduct
    template_name = 'dashboard/subscription_product_list.html'
    context_object_name = 'subscription_products'


class SubscriptionProductCreateView(StaffRequiredMixin, CreateView):
    model = SubscriptionProduct
    form_class = SubscriptionProductForm
    template_name = 'dashboard/subscription_product_form.html'
    success_url = reverse_lazy('dashboard:subscription_management')


class SubscriptionProductUpdateView(StaffRequiredMixin, UpdateView):
    model = SubscriptionProduct
    form_class = SubscriptionProductForm
    template_name = 'dashboard/subscription_product_form.html'
    success_url = reverse_lazy('dashboard:subscription_management')


class SubscriptionProductDeleteView(StaffRequiredMixin, DeleteView):
    model = SubscriptionProduct
    template_name = 'dashboard/subscription_product_confirm_delete.html'
    success_url = reverse_lazy('dashboard:subscription_management')


class SubscribedUsersListView(StaffRequiredMixin, ListView):
    model = Profile
    template_name = 'dashboard/subscribed_users_list.html'
    context_object_name = 'subscriptions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = Profile.objects.filter(is_subscribed=True)

        for profile in subscriptions:
            if profile.is_subscribed and profile.subscription_start_date:
                expiration_date = (
                    profile.subscription_start_date + timedelta(days=365)
                )
                profile.time_remaining = (
                    expiration_date - timezone.now().date()
                )
            else:
                profile.time_remaining = "No active subscription"
        context['subscriptions'] = subscriptions
        return context


class UpdateSubscriptionStatusView(StaffRequiredMixin, View):
    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        profile.is_subscribed = not profile.is_subscribed
        profile.subscription_start_date = (
            None if not profile.is_subscribed
            else profile.subscription_start_date
        )
        profile.save()
        messages.success(request, 'Subscription status updated successfully.')
        return redirect('dashboard:subscribed_users_list')


class NewsletterRecipientsView(StaffRequiredMixin, ListView):
    model = Profile
    template_name = 'dashboard/newsletter_recipients.html'
    context_object_name = 'newsletter_recipients'

    def get_queryset(self):
        return Profile.objects.filter(newsletter_recipient=True)
