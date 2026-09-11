from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_time"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject"]
