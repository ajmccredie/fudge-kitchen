from django import forms
from edible_products.models import EdibleProduct, ProductWeightPrice

class EdibleProductForm(forms.ModelForm):
    class Meta:
        model = EdibleProduct
        fields = ['flavour', 'details', 'ingredients', 'quantity', 'weight', 'price', 'image', 'gluten', 'crustaceans', 'eggs', 'fish', 'peanuts', 'soybeans', 'milk', 'nuts', 'celery', 'mustard', 'sesame_seeds', 'sulphur_dioxide_and_sulphites', 'lupin', 'molluscs']

    def __init__(self, *args, **kwargs):
        super(EdibleProductForm, self).__init__(*args, **kwargs)
        default_prices = EdibleProduct.DEFAULT_WEIGHT_PRICES

        for weight, price in default_prices.items():
            field_name = f'price_{weight}g'
            self.fields[field_name] = forms.DecimalField(
                initial=price,
                label=f'Price for {weight}g (override)',
                required=False
            )

    def save(self, commit=True):
        instance = super(EdibleProductForm, self).save(commit=False)
        
        if commit:
            instance.save()
            self.save_m2m()  # To save many-to-many data
            for weight, price in EdibleProduct.DEFAULT_WEIGHT_PRICES.items():
                field_name = f'price_{weight}g'
                weight_price = self.cleaned_data.get(field_name) or price
                ProductWeightPrice.objects.update_or_create(
                    product=instance,
                    weight=weight,
                    defaults={'price': weight_price}
                )

        return instance