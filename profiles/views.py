from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import HttpResponse
from django.views import View

class ProfileView(View):
    """ Display the user's profile. """

    def get(self, request, *args, **kwargs):
        # Your logic to retrieve user profile data
        profile_data = {}  # Replace this with your actual logic
        
        template = 'profiles/profile.html'
        context = {
            'profile_data': profile_data,
        }
        return render(request, template, context)


@login_required
class EditProfileView(View):
    template_name = 'profiles/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
