from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field

class ProfileForm(forms.ModelForm):
    ALLERGEN_FIELDS = [
        ('gluten', 'Gluten'), ('crustaceans', 'Crustaceans'), ('eggs', 'Eggs'),
        ('fish', 'Fish'), ('peanuts', 'Peanuts'), ('soybeans', 'Soybeans'),
        ('milk', 'Milk'), ('nuts', 'Nuts'), ('celery', 'Celery'), ('mustard', 'Mustard'),
        ('sesame_seeds', 'Sesame Seeds'), ('sulphur_dioxide_and_sulphites', 'Sulphur Dioxide and Sulphites'),
        ('lupin', 'Lupin'), ('molluscs', 'Molluscs')
    ]

    allergens = forms.MultipleChoiceField(
        choices=ALLERGEN_FIELDS,
        widget=forms.CheckboxSelectMultiple(),
        label="Allergen Preferences",
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'dietary_preference', 'default_phone_number', 'default_country', 'default_postcode',
            'default_town_or_city', 'default_street_address1', 'default_street_address2',
            'default_county', 'newsletter_recipient'
        ]
        labels = {
            'dietary_preference': 'Dietary Preference',
            'default_phone_number': 'Phone Number',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'newsletter_recipient': 'Receiver of our awesome newsletter',
        }
        widgets = {
            'dietary_preference': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('dietary_preference', css_class='form-group col-md-6 mb-0'),
                Column('default_phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('default_country', css_class='form-group col-md-6 mb-0'),
                Column('default_postcode', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('default_town_or_city', css_class='form-group col-md-6 mb-0'),
                Column('default_street_address1', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('default_street_address2', css_class='form-group col-md-6 mb-0'),
                Column('default_county', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('newsletter_recipient', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('allergens', css_class='form-group col-12'),
            Submit('submit', 'Update Profile', css_class='btn btn-primary')
        )

        if self.instance:
            self.initial['allergens'] = [
                field_name for field_name, _ in self.ALLERGEN_FIELDS
                if getattr(self.instance, field_name)
            ]

    def save(self, commit=True):
        profile = super().save(commit=False)
        for field_name, _ in self.ALLERGEN_FIELDS:
            setattr(profile, field_name, False)
        if 'allergens' in self.cleaned_data:
            for allergen in self.cleaned_data['allergens']:
                setattr(profile, allergen, True)
        if commit:
            profile.save()
        return profile
