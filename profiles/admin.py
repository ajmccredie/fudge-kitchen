from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'
    fields = ['allergen_preferences', 'default_phone_number', 'default_country', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2', 'default_county', 'is_subscribed', 'newsletter_recipient']
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_subscribed_admin', 'newsletter_recipient_admin')

    def is_subscribed_admin(self, instance):
        return instance.profile.is_subscribed if hasattr(instance, 'profile') else False
    is_subscribed_admin.boolean = True
    is_subscribed_admin.short_description = 'Paid Subscription'

    def newsletter_recipient_admin(self, instance):
        return instance.profile.newsletter_recipient if hasattr(instance, 'profile') else False
    newsletter_recipient_admin.boolean = True
    newsletter_recipient_admin.short_description = 'Newsletter Recipient'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'profile'):
            Profile.objects.create(user=obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
