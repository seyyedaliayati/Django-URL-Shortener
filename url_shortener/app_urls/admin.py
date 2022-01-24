from django.contrib import admin

from .models import Click, Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('alias', 'url', 'date_created', )
    search_fields = ('url', )


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('link', 'ip_address', 'clicks_count', 'clicked_date', )
