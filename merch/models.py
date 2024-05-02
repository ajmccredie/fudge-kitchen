from django.db import models
from django.urls import reverse

class MerchProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=50) # 'coaster', 'mug', 'water bottle', 'tote bag'
    image = models.ImageField(upload_to='merch_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merch_product_detail', args=[str(self.id)])


class ColourVariation(models.Model):
    product = models.ForeignKey(MerchProduct, related_name='colours', on_delete=models.CASCADE)
    colour_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='colour_variations/')

    def __str__(self):
        return f"{self.product.name} - {self.colour_name}"

class TextOption(models.Model):
    product = models.ForeignKey(MerchProduct, related_name='text_options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='merch_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.text}"