from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, new = Profile.objects.get_or_create(user=instance)
    print(f"Profile created: {new}")
    if created:
        profile.default_phone_number = '0123456789'
        profile.default_country = 'GB'
        profile.default_postcode = 'Default Postcode'
        profile.default_town_or_city = 'Default City'
        profile.default_street_address1 = 'Default Address 1'
        profile.default_street_address2 = 'Default Address 2'
        profile.default_county = 'Default County'
        profile.is_subscribed = False
        profile.save()
        print(f"Profile for user {instance.username} created with defaults.")
    else:
        print(
            f"{instance.username} already exists, no profile created."
            )
