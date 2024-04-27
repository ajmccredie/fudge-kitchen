from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'
    fields = ['allergen_preferences', 'default_phone_number', 'default_country', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2', 'default_county', 'is_subscribed']
    extra = 0  # Prevents extra empty forms

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'profile'):
            Profile.objects.create(user=obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
