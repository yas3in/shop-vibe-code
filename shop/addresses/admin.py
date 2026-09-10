from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['receipt_name', 'user', 'city', 'is_default']
    list_filter = ['city', 'is_default']
