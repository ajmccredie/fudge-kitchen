from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django_countries.fields import CountryField
from core.models import Product, CommonProduct


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    symbol = models.ImageField(upload_to='allergens/', null=True, blank=True)

    def __str__(self):
        return self.name


class SubscriptionProduct(Product):
    duration_in_years = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        CommonProduct.objects.get_or_create(product_type='subscription', product_id=self.id)


class Profile(models.Model):
    """ 
    This will store the important information for the user
    which they can access on login
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    allergen_preferences = models.ManyToManyField(Allergen, blank=True)
    dietary_preference = models.CharField(max_length=20, blank=True, null=True, help_text='Would you prefer to only see plant-based options?')
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_start_date = models.DateField(null=True, blank=True)
    newsletter_recipient = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username}'s profile"

    def has_active_subscription(self):
        if not self.is_subscribed or not self.subscription_start_date:
            return False
        expiration_date = self.subscription_start_date + timezone.timedelta(days=365 * 1)
        return timezone.now().date() < expiration_date

    def get_subscription_time_remaining(self):
        if not self.is_subscribed or not self.subscription_start_date:
            return "No active subscription"
        expiration_date = self.subscription_start_date + timezone.timedelta(days=365 * 1)
        print(f"Expiration Date: {expiration_date}, Current Date: {timezone.now().date()}")
        return expiration_date - timezone.now().date()



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create of update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
