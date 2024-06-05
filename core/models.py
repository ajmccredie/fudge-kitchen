from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('edible', 'Edible'),
        ('merch', 'Merch'),
        ('subscription', 'Subscription'),
    ]

    name = models.CharField(
        max_length=254,
        blank=False,
        null=False,
        default="Product Name"
        )
    description = models.TextField(
        max_length=600,
        blank=False,
        null=False,
        default="Product Description"
        )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=True,
        default=7.00
        )
    image = models.ImageField(
        null=False,
        blank=False,
        default='static/images/default_text_logo.png'
        )
    product_type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPE_CHOICES,
        blank=True,
        null=True
        )

    def __str__(self):
        return self.name

    def get_price(self):
        """Get the price of the product."""
        return self.price

    class Meta:
        abstract = True


class ProductReference(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.content_type} - {self.object_id}"


class CommonProduct(models.Model):
    product_type = models.CharField(max_length=50)
    product_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_type} - {self.product_id}"
