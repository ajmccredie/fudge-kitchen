from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    symbol = models.ImageField(upload_to='allergens/', null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """ 
    This will store the important information for the user
    which they can access on login
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    allergen_preferences = models.ManyToManyField(Allergen, blank=True)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255, blank=True)
    billing_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create of update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()