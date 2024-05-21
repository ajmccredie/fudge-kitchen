from django.db import models
from django.urls import reverse
from core.models import Product
from django.core.exceptions import ValidationError

class MerchProduct(Product):
    type = models.CharField(max_length=50)  # 'coaster', 'mug', 'water bottle', 'tote bag'
    colour = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merch_product_detail', args=[self.pk])

class ColourVariation(models.Model):
    product = models.ForeignKey(MerchProduct, related_name='colours', on_delete=models.CASCADE)
    colour_name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    url_product = models.ForeignKey(MerchProduct, related_name='url_products', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.colour_name}"

    def get_absolute_url(self):
        if self.url_product:
            return reverse('merch_product_detail', args=[self.url_product.pk])
        return reverse('merch_product_detail', args=[self.product.pk])


class TextOption(models.Model):
    product = models.ForeignKey(MerchProduct, related_name='text_options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    is_default = models.BooleanField(default=False, help_text="This will be the default phrase for this product")

    def __str__(self):
        return f"{self.text}"

    def clean(self):
        if self.is_default:
            other_defaults = TextOption.objects.filter(product=self.product, is_default=True).exclude(pk=self.pk)
            if other_defaults.exists():
                raise ValidationError('There can be only one default text option per product.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

