from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    allergen_preferences = models.CharField(max_length=255, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"