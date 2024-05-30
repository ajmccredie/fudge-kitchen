from django.contrib import admin
from .models import MerchProduct, ColourVariation, TextOption


@admin.register(ColourVariation)
class ColourVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'colour_name', 'image', 'get_url')
    search_fields = ('product__name', 'colour_name')
    list_filter = ('product',)

    def get_url(self, obj):
        return obj.get_absolute_url()
    get_url.short_description = 'URL'
    get_url.admin_order_field = 'url_product'


class ColourVariationInline(admin.TabularInline):
    model = ColourVariation
    extra = 2
    fk_name = 'product'


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
