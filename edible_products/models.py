from django.db import models


class EdibleProduct(models.Model):
    plant_based = models.BooleanField(default=False)
    flavour = models.CharField(max_length=254, null=True, blank=True)
    guest_flavour = models.BooleanField(default=False)
    details = models.TextField()
    ingredients = models.TextField()
    quantity = models.IntegerField()
    weight = models.DecimalField(default=400, max_digits=4, decimal_places=0, help_text="Weight in grams")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # Allergens as boolean fields
    gluten = models.BooleanField(default=False, verbose_name='Gluten')
    crustaceans = models.BooleanField(default=False, verbose_name='Crustaceans')
    eggs = models.BooleanField(default=False, verbose_name='Eggs')
    fish = models.BooleanField(default=False, verbose_name='Fish')
    peanuts = models.BooleanField(default=False, verbose_name='Peanuts')
    soybeans = models.BooleanField(default=False, verbose_name='Soybeans')
    milk = models.BooleanField(default=False, verbose_name='Milk')
    nuts = models.BooleanField(default=False, verbose_name='Nuts')
    celery = models.BooleanField(default=False, verbose_name='Celery')
    mustard = models.BooleanField(default=False, verbose_name='Mustard')
    sesame_seeds = models.BooleanField(default=False, verbose_name='Sesame Seeds')
    sulphur_dioxide_and_sulphites = models.BooleanField(default=False, verbose_name='Sulphur Dioxide and Sulphites')
    lupin = models.BooleanField(default=False, verbose_name='Lupin')
    molluscs = models.BooleanField(default=False, verbose_name='Molluscs')

    def __str__(self):
        return self.flavour

    def list_allergens(self):
        """Returns a list of allergens present in the product."""
        allergens = []
        fields = [
            ('gluten', 'Gluten'), ('crustaceans', 'Crustaceans'), ('eggs', 'Eggs'), 
            ('fish', 'Fish'), ('peanuts', 'Peanuts'), ('soybeans', 'Soybeans'),
            ('milk', 'Milk'), ('nuts', 'Nuts'), ('celery', 'Celery'), ('mustard', 'Mustard'),
            ('sesame_seeds', 'Sesame Seeds'), ('sulphur_dioxide_and_sulphites', 'Sulphur Dioxide and Sulphites'),
            ('lupin', 'Lupin'), ('molluscs', 'Molluscs')
        ]
        for field_name, human_readable in fields:
            if getattr(self, field_name):
                allergens.append(human_readable)
        return ", ".join(allergens) if allergens else "No Allergens"
