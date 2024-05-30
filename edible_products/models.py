from django.db import models
from core.models import Product, CommonProduct


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    symbol = models.ImageField(upload_to='allergens/', null=True, blank=True)

    def __str__(self):
        return self.name


class EdibleProduct(Product):
    WEIGHT_CHOICES = [
        (100, '100g'),
        (400, '400g'),
        (800, '800g'),
    ]

    DEFAULT_WEIGHT_PRICES = {
        100: 3.50,
        400: 7.00,
        800: 11.00,
    }

    plant_based = models.BooleanField(default=False)
    description = models.TextField(blank=False, null=True)
    flavour = models.CharField(max_length=254, null=True, blank=False)
    guest_flavour = models.BooleanField(default=False)
    ingredients = models.TextField()
    weight = models.PositiveIntegerField(
        default=400, choices=WEIGHT_CHOICES, help_text="Weight in grams"
    )
    image_url = models.URLField(max_length=1024, null=True, blank=False)

    # Allergen boolean fields
    gluten = models.BooleanField(default=False, verbose_name='Gluten')
    crustaceans = models.BooleanField(
        default=False, verbose_name='Crustaceans'
        )
    eggs = models.BooleanField(default=False, verbose_name='Eggs')
    fish = models.BooleanField(default=False, verbose_name='Fish')
    peanuts = models.BooleanField(default=False, verbose_name='Peanuts')
    soybeans = models.BooleanField(
        default=False, verbose_name='Soybeans'
        )
    milk = models.BooleanField(default=False, verbose_name='Milk')
    nuts = models.BooleanField(default=False, verbose_name='Nuts')
    celery = models.BooleanField(default=False, verbose_name='Celery')
    mustard = models.BooleanField(default=False, verbose_name='Mustard')
    sesame_seeds = models.BooleanField(
        default=False, verbose_name='Sesame Seeds'
        )
    sulphur_dioxide_and_sulphites = models.BooleanField(
        default=False, verbose_name='Sulphur Dioxide and Sulphites'
    )
    lupin = models.BooleanField(default=False, verbose_name='Lupin')
    molluscs = models.BooleanField(default=False, verbose_name='Molluscs')

    allergens = models.ManyToManyField(Allergen, blank=True)

    def __str__(self):
        return f"{self.name} - {self.flavour} ({self.weight}g)"

    def get_price_for_weight(self, weight):
        """Retrieve price for a specific weight from the
        ProductWeightPrice model."""
        try:
            price_record = self.weight_prices.get(weight=weight)
            return price_record.price
        except ProductWeightPrice.DoesNotExist:
            return None

    def list_allergens(self):
        """Returns a list of allergens present in the product based
        on boolean fields."""
        allergens = []
        fields = [
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
            ('molluscs', 'Molluscs')
        ]
        for field_name, human_readable in fields:
            if getattr(self, field_name):
                allergens.append(human_readable)
        return ", ".join(allergens) if allergens else "No Allergens"

    def get_allergens_info(self):
        """Returns a list of dictionaries for present
        allergens with their names and symbol paths."""
        allergens_info = []
        allergen_fields = [
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
            ('molluscs', 'Molluscs')
        ]
        for field_name, human_readable in allergen_fields:
            if getattr(self, field_name):
                allergens_info.append({
                    'name': human_readable,
                    'symbol_path': f'images/{field_name}.png'
                })

        return allergens_info

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            for weight, price in self.DEFAULT_WEIGHT_PRICES.items():
                ProductWeightPrice.objects.create(
                    product=self, weight=weight, price=price
                )
            CommonProduct.objects.create(
                product_type='edible', product_id=self.id
            )
        else:
            common_product = CommonProduct.objects.filter(
                product_type='edible', product_id=self.id
            ).first()
            if common_product:
                common_product.save()
            else:
                CommonProduct.objects.create(
                    product_type='edible', product_id=self.id
                )


class ProductWeightPrice(models.Model):
    product = models.ForeignKey(
        EdibleProduct, related_name='weight_prices', on_delete=models.CASCADE
    )
    weight = models.IntegerField(help_text="Weight in grams")
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.weight}g - £{self.price}"
