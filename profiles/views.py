from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from .models import Profile, SubscriptionProduct
from checkout.models import Order
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import CommonProduct


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profiles/profile.html'
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(instance=profile)
        orders = profile.orders.order_by('-date')
        latest_order = orders.first()
        allergen_info = {
            field: getattr(profile, field)
            for field, _
            in ProfileForm.ALLERGEN_FIELDS
            }
        dietary_preference = profile.get_dietary_preference_display()

        context = {
            'form': form,
            'orders': orders,
            'latest_order': latest_order,
            'on_profile_page': True,
            'subscription_active': profile.is_subscribed,
            'subscription_start_date': profile.subscription_start_date,
            'subscription_time_remaining': (
                profile.get_subscription_time_remaining()
                ),
            'allergen_info': allergen_info,
            'dietary_preference': dietary_preference,
            'newsletter_recipient': profile.newsletter_recipient,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request,
                'Cannot update: Please check the form for errors.'
                )
        orders = profile.orders.order_by('-date')
        latest_order = orders.first()

        allergen_info = {
            field: getattr(profile, field)
            for field, _
            in ProfileForm.ALLERGEN_FIELDS
            }
        dietary_preference = profile.get_dietary_preference_display()

        context = {
            'form': form,
            'orders': orders,
            'latest_order': latest_order,
            'on_profile_page': True,
            'subscription_active': profile.is_subscribed,
            'subscription_start_date': profile.subscription_start_date,
            'subscription_time_remaining': (
                profile.get_subscription_time_remaining()
            ),
            'allergen_info': allergen_info,
            'dietary_preference': dietary_preference,
            'newsletter_recipient': profile.newsletter_recipient,
        }
        return render(request, self.template_name, context)


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'profiles/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profiles:profile')
        else:
            messages.error(
                request,
                'Cannot update: Please check the form for errors.'
                )
        return render(request, self.template_name, {'form': form})


class DeleteProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        logout(request)  # Logout the user after account deletion
        messages.success(request, "Account successfully deleted.")
        return redirect('home')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'profiles/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context['order']
        context['line_items'] = order.lineitems.all()
        return context


class SubscriptionView(View):
    def get(self, request):
        print("SubscriptionView: GET request received")
        subscription_product = (
            get_object_or_404(
                SubscriptionProduct,
                name="Annual Subscription"
                )
        )
        common_product = (
            CommonProduct.objects.get
            (product_id=subscription_product.id,
                product_type='subscription')
        )

        return render(request, 'profiles/subscription_page.html', {
            'subscription_product': subscription_product,
            'common_product': common_product,
        })


class AddSubscriptionToBasketView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            subscription_product = SubscriptionProduct.objects.get()
        except SubscriptionProduct.DoesNotExist:
            messages.error(request, 'Subscription product not found.')
            return redirect('profiles:subscription')

        if request.user.profile.is_subscribed:
            messages.error(request, 'You already have an active subscription.')
            return redirect('profiles:subscription')

        basket = request.session.get('basket', {})
        basket = {
            k: v for k, v in basket.items()
            if CommonProduct.objects.get(pk=k).product_type !=
            'subscription'
            }

        common_product = CommonProduct.objects.get(
            product_id=subscription_product.id,
            product_type='subscription'
            )

        basket[str(common_product.id)] = {
            'product_id': subscription_product.id,
            'product_type': 'subscription',
            'quantity': 1,
            'price': str(subscription_product.price),
            'name': subscription_product.name,
            'image_url': subscription_product.image.url
        }

        request.session['basket'] = basket
        request.session.modified = True
        messages.success(
            request, f'Added "{subscription_product.name}" to your basket.'
            )
        return redirect('basket:view_basket')
