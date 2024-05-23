from django import forms
from django.forms import inlineformset_factory
from edible_products.models import EdibleProduct, ProductWeightPrice, Allergen
from merch.models import MerchProduct, ColourVariation, TextOption
from checkout.models import Order, OrderLineItem
from profiles.models import SubscriptionProduct


class EdibleProductForm(forms.ModelForm):
    plant_based = forms.BooleanField(label='Plant-based', required=False)
    allergens = forms.ModelMultipleChoiceField(queryset=Allergen.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = EdibleProduct
        fields = ['name', 'flavour', 'description', 'ingredients', 'image', 'gluten', 'crustaceans', 'eggs', 'fish', 'peanuts', 'soybeans', 'milk', 'nuts', 'celery', 'mustard', 'sesame_seeds', 'sulphur_dioxide_and_sulphites', 'lupin', 'molluscs', 'plant_based']

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
        instance.plant_based = self.cleaned_data.get('plant_based', False)

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


class MerchProductForm(forms.ModelForm):
    class Meta:
        model = MerchProduct
        fields = ['name', 'description', 'price', 'type', 'colour', 'image']

    def __init__(self, *args, **kwargs):
        super(MerchProductForm, self).__init__(*args, **kwargs)

# Specify the fk_name attribute
ColourVariationFormSet = inlineformset_factory(
    MerchProduct,
    ColourVariation,
    fields=('colour_name', 'image', 'url_product'),
    extra=1,
    can_delete=True,
    fk_name='product'
)

TextOptionFormSet = inlineformset_factory(
    MerchProduct,
    TextOption,
    fields=('text', 'image'),
    extra=1,
    can_delete=True,
    fk_name='product'
)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['dispatched']

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['made']


class SubscriptionProductForm(forms.ModelForm):
    class Meta:
        model = SubscriptionProduct
        fields = ['name', 'description', 'price', 'image']