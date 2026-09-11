from django.conf import settings
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )
    logo = models.ImageField(upload_to="brands/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def descendant_ids(self):
        ids, stack = [], [self.pk]
        while stack:
            current = stack.pop()
            ids.append(current)
            stack.extend(Category.objects.filter(parent_id=current).values_list("pk", flat=True))
        return ids


class ProductType(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_type} - {self.name}"


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductPrice(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE, related_name="price")
    price = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.product} - {self.final_price}"

    @property
    def final_price(self):
        return self.price - (self.price * self.discount_percent // 100)


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    product_type = models.ForeignKey(
        ProductType, on_delete=models.PROTECT, related_name="products"
    )
    attributes = models.ManyToManyField(ProductAttributeValue, related_name="products", blank=True)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    base_image = models.ImageField(upload_to="products/", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        return self.price.final_price if hasattr(self, "price") else None

    @property
    def discount_percent(self):
        return self.price.discount_percent if hasattr(self, "price") else 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product} #{self.pk}"


class Basket(models.Model):
    STATUS_CHOICES = (
        ("expired", "منقضی شده"),
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده")
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="baskets"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True)

    def __str__(self):
        return f"سبد {self.user} #{self.pk}"

    @property
    def total_quantity(self):
        return sum(line.quantity for line in self.lines.all())

    total_items = total_quantity

    @property
    def total_price(self):
        return sum(line.line_final_price for line in self.lines.all())

    @property
    def total_original_price(self):
        return sum(line.line_total for line in self.lines.all())

    @property
    def total_discount(self):
        return self.total_original_price - self.total_price


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_lines")
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product} - {self.quantity}"

    @property
    def unit_price(self):
        return self.product.price.price

    @property
    def unit_final_price(self):
        return self.product.final_price

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    @property
    def line_final_price(self):
        return self.unit_final_price * self.quantity
