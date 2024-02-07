from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['allergen_preferences', 'shipping_address', 'billing_address', 'is_subscribed']
