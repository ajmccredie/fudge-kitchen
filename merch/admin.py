from django.contrib import admin
from .models import MerchProduct, ColourVariation, TextOption

# Register your models here.

class ColourVariationInline(admin.TabularInline):
    model = ColourVariation
    extra = 1

class MerchProductAdmin(admin.ModelAdmin):
    inlines = [ColourVariationInline]

admin.site.register(MerchProduct, MerchProductAdmin)

