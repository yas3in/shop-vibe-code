from django.contrib import admin
from .models import (
    Brand, Category, ProductType, ProductAttribute,
    ProductAttributeValue, Product, ProductPrice,
    ProductImage, Basket, BasketLine,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active']
    list_filter = ['is_active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['value', 'product_attribute']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'brand', 'stock', 'is_active']
    list_filter = ['is_active', 'category', 'brand']
    search_fields = ['title']
    inlines = [ProductPriceInline, ProductImageInline]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_time']
    list_filter = ['status']
