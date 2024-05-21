from django.db import models

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('edible', 'Edible'),
        ('merch', 'Merch'),
        ('subscription', 'Subscription'),
    ]

    name = models.CharField(max_length=254, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_price(self):
        """Get the price of the product."""
        return self.price

    class Meta:
        abstract = True