from django.contrib import admin

from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "receipt_name", "phone_number", "city", "is_default"]
    list_filter = ["city", "is_default"]
    search_fields = ["user__username", "receipt_name", "phone_number"]
