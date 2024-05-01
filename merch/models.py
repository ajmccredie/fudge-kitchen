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
