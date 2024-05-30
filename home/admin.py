from django.contrib import admin
from .models import OurStory


@admin.register(OurStory)
class OurStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated')
    search_fields = ('title', 'content')
