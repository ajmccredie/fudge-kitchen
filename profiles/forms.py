from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        fields = ['allergen_preferences', 'dietary_preference', 'default_phone_number', 'default_country', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2', 'default_county', 'is_subscribed', 'newsletter_recipient']
        widgets = {
            'allergen_preferences': forms.CheckboxSelectMultiple(),
            'dietary_preference': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': "Phone number",
            'default_postcode': "Postal Code",
            'default_town_or_city': "Town or City",
            'default_street_address1': "Street Address 1",
            'default_street_address2': "Street Address 2",
            'default_county': "County, State or Locality",
            'is_subscribed': 'Monthly subscription for free delivery and treats',
        }
        for field in self.fields:
            if field != 'default_country':
                placeholder = placeholders.get(field, '') 
                self.fields[field].widget.attrs['placeholder'] = placeholder if self.fields[field].required else f'{placeholder} (optional)'
                self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
                self.fields[field].label = False
            if field == 'is_subscribed':
                self.fields[field].widget.attrs['disabled'] = 'disabled'
