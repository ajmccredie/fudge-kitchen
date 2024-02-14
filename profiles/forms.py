from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        fields = fields = ['allergen_preferences', 'default_phone_number', 'default_country', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2', 'default_county']

    def __init__(self, *args, **kwargs):
        """ 
        Default placeholders are used waiting for user input
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'allergen_preferences': "allergens", 
            'default_phone_number': "Phone mumber",
            'default_postcode': "Postal Code",
            'default_town_or_city': "Towm or City",
            'default_street_address1': "Street Address 1",
            'default_street_address2': "Street Address 2",
            'default_county': "County, State or Locality",
        }
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
