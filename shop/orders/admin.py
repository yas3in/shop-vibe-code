from django.contrib import admin
from .models import Order, OrderLine, Payment


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = ['product', 'product_title', 'quantity', 'price']


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'user', 'status', 'total_price', 'created_time']
    list_filter = ['status']
    inlines = [OrderLineInline, PaymentInline]
