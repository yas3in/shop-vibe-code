from django.contrib import admin


from .models import (Brand, Category, Product, ProductAttribute, ProductAttributeValue,
    ProductImage, ProductPrice, ProductType,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "product_type"]
    list_filter = ["product_type"]


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ["value", "product_attribute"]
    list_filter = ["product_attribute__product_type"]
    search_fields = ["value"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    max_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "brand", "stock", "sold_count", "is_active"]
    list_filter = ["is_active", "category", "brand"]
    search_fields = ["title"]
    inlines = [ProductPriceInline, ProductImageInline]
    filter_horizontal = ["attributes"]


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ["product", "price", "discount_percent"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]
