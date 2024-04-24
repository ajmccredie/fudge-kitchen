from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(View):
    """ Display the user's profile. """
    template_name = 'profiles/profile.html'
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(instance=profile)
        orders = profile.orders.all()
        context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        orders = profile.orders.all()
        context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True
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
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class DeleteProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        logout(request)  # Logout the user after account deletion
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')