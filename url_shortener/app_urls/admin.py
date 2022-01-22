from django.contrib import admin

from .models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('alias', 'url', 'clicks_count', 'date_created', )
    search_fields = ('url', )
