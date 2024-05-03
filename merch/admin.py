from django.contrib import admin
from .models import MerchProduct, ColourVariation, TextOption

# Register your models here.

class ColourVariationInline(admin.TabularInline):
    model = ColourVariation
    extra = 2

class TextOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'text', 'image')

admin.site.register(TextOption, TextOptionAdmin)

class TextOptionInline(admin.TabularInline):
    model = TextOption
    extra = 3

class MerchProductAdmin(admin.ModelAdmin):
    inlines = [ColourVariationInline, TextOptionInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(MerchProduct, MerchProductAdmin)