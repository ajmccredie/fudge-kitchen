from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    ALLERGEN_FIELDS = [
        ('gluten', 'Gluten'), ('crustaceans', 'Crustaceans'), ('eggs', 'Eggs'),
        ('fish', 'Fish'), ('peanuts', 'Peanuts'), ('soybeans', 'Soybeans'),
        ('milk', 'Milk'), ('nuts', 'Nuts'), ('celery', 'Celery'), ('mustard', 'Mustard'),
        ('sesame_seeds', 'Sesame Seeds'), ('sulphur_dioxide_and_sulphites', 'Sulphur Dioxide and Sulphites'),
        ('lupin', 'Lupin'), ('molluscs', 'Molluscs')
    ]

    class Meta:
        model = Profile
        fields = [
            'dietary_preference', 'default_phone_number', 'default_country', 'default_postcode',
            'default_town_or_city', 'default_street_address1', 'default_street_address2',
            'default_county', 'is_subscribed', 'newsletter_recipient'
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
            'is_subscribed': 'Part of the subscriber family',
            'newsletter_recipient': 'Receiver of our awesome newsletter',
        }
        widgets = {
            'dietary_preference': forms.RadioSelect(),
        }

    allergens = forms.MultipleChoiceField(
        choices=ALLERGEN_FIELDS,
        widget=forms.CheckboxSelectMultiple(),
        label="Allergen Preferences",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.label = self.Meta.labels.get(field_name, field_name.replace('_', ' ').capitalize())
            if field.required:
                field.widget.attrs['placeholder'] = f"{field.label} *"
            else:
                field.widget.attrs['placeholder'] = field.label

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