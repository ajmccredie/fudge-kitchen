from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django_countries.fields import CountryField
from core.models import Product, CommonProduct


class SubscriptionProduct(Product):
    duration_in_years = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        CommonProduct.objects.get_or_create(
            product_type='subscription',
            product_id=self.id
        )


class Profile(models.Model):
    DIETARY_CHOICES = [
        ('none', 'None'),
        ('plant_based', 'Plant Based'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    dietary_preference = models.CharField(max_length=20,
                                          choices=DIETARY_CHOICES,
                                          default='none')
    default_phone_number = models.CharField(max_length=20, null=True,
                                            blank=True)
    default_country = CountryField(blank_label='Country *', null=True,
                                   blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_start_date = models.DateField(null=True, blank=True)
    newsletter_recipient = models.BooleanField(default=False)

    # Allergen boolean fields
    gluten = models.BooleanField(default=False, verbose_name='Gluten')
    crustaceans = models.BooleanField(default=False,
                                      verbose_name='Crustaceans')
    eggs = models.BooleanField(default=False, verbose_name='Eggs')
    fish = models.BooleanField(default=False, verbose_name='Fish')
    peanuts = models.BooleanField(default=False, verbose_name='Peanuts')
    soybeans = models.BooleanField(default=False, verbose_name='Soybeans')
    milk = models.BooleanField(default=False, verbose_name='Milk')
    nuts = models.BooleanField(default=False, verbose_name='Nuts')
    celery = models.BooleanField(default=False, verbose_name='Celery')
    mustard = models.BooleanField(default=False, verbose_name='Mustard')
    sesame_seeds = models.BooleanField(default=False,
                                       verbose_name='Sesame Seeds')
    sulphur_dioxide_and_sulphites = models.BooleanField(
        default=False,
        verbose_name='Sulphur Dioxide and Sulphites'
    )
    lupin = models.BooleanField(default=False, verbose_name='Lupin')
    molluscs = models.BooleanField(default=False, verbose_name='Molluscs')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def has_active_subscription(self):
        if not self.is_subscribed or not self.subscription_start_date:
            return False
        expiration_date = (
            self.subscription_start_date + timedelta(days=365 * 1)
        )
        return timezone.now().date() < expiration_date

    def get_subscription_time_remaining(self):
        if not self.is_subscribed or not self.subscription_start_date:
            return "No active subscription"
        expiration_date = (
            self.subscription_start_date + timedelta(days=365 * 1)
        )
        return expiration_date - timezone.now().date()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
