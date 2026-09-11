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
    list_display = ["product", "product_attribute", "value"]
    list_filter = ["product_attribute__product_type"]
    search_fields = ["value", "product__title"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    max_num = 1


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 2

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product_attribute":
            match = request.resolver_match
            object_id = match.kwargs.get("object_id") if match else None
            if object_id:
                product = Product.objects.filter(pk=object_id).select_related("product_type").first()
                if product:
                    kwargs["queryset"] = ProductAttribute.objects.filter(product_type=product.product_type)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "brand", "stock", "sold_count", "is_active"]
    list_filter = ["is_active", "category", "brand"]
    search_fields = ["title"]
    inlines = [ProductPriceInline, ProductImageInline, ProductAttributeValueInline]


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ["product", "price", "discount_percent"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]
