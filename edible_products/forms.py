from django import forms


class AllergenFilterForm(forms.Form):
    ALLERGEN_CHOICES = [
        ('gluten', 'Gluten'),
        ('crustaceans', 'Crustaceans'),
        ('eggs', 'Eggs'),
        ('fish', 'Fish'),
        ('peanuts', 'Peanuts'),
        ('soybeans', 'Soybeans'),
        ('milk', 'Milk'),
        ('nuts', 'Nuts'),
        ('celery', 'Celery'),
        ('mustard', 'Mustard'),
        ('sesame_seeds', 'Sesame Seeds'),
        ('sulphur_dioxide_and_sulphites', 'Sulphur Dioxide and Sulphites'),
        ('lupin', 'Lupin'),
        ('molluscs', 'Molluscs'),
    ]
    allergens = forms.MultipleChoiceField(
        choices=ALLERGEN_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Exclude Allergens:"
    )
