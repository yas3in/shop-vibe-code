from django.contrib import admin

from catalog.models import Basket, BasketLine
from .models import Order, OrderItem, Payment


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    extra = 0


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ["ref_id", "amount", "order", "status"]
    can_delete = False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_title", "unit_price", "quantity"]
    can_delete = False


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "created_time"]
    list_filter = ["status"]
    inlines = [BasketLineInline]


@admin.register(BasketLine)
class BasketLineAdmin(admin.ModelAdmin):
    list_display = ["basket", "product", "quantity"]


class OrderLineInline(PaymentInline):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["ref_id", "user", "status", "total_price", "created_time"]
    list_filter = ["status"]
    search_fields = ["ref_id", "user__username"]
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ["ref_id", "total_price"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product_title", "quantity", "unit_price"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["ref_id", "order", "amount", "status", "created_time"]
    list_filter = ["status"]


admin.site.site_header = "مدیریت ایرشاپ"
admin.site.site_title = "ایرشاپ"
admin.site.index_title = "پنل مدیریت"
