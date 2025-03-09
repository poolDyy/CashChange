from django.contrib import admin

from .models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    """Админка валюты."""

    list_display = ['id', 'code', 'title']
    search_fields = ['code', 'title']


admin.site.register(Currency, CurrencyAdmin)
