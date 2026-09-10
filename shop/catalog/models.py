from django.db import models


class Brand(models.Model):
    name = models.CharField("نام برند", max_length=100, unique=True)
    parent = models.ForeignKey(
        "self", verbose_name="برند والد", on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )
    logo = models.ImageField("لوگو", upload_to="brands/", null=True, blank=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("نام دسته", max_length=100)
    parent = models.ForeignKey(
        "self", verbose_name="دسته والد", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    slug = models.SlugField("نامک", max_length=120, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

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
    title = models.CharField("عنوان نوع محصول", max_length=100, unique=True)
    description = models.TextField("توضیحات", blank=True)

    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصول"

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType, verbose_name="نوع محصول", on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField("نام ویژگی", max_length=100)

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی‌های محصول"
        unique_together = [("product_type", "name")]

    def __str__(self):
        return f"{self.product_type} - {self.name}"


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(
        ProductAttribute, verbose_name="ویژگی", on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField("مقدار", max_length=255)

    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی"

    def __str__(self):
        return self.value


class ProductPrice(models.Model):
    product = models.OneToOneField("Product", verbose_name="محصول", on_delete=models.CASCADE, related_name="price")
    price = models.PositiveIntegerField("قیمت (تومان)", default=0)
    discount_percent = models.PositiveSmallIntegerField("درصد تخفیف", default=0)

    class Meta:
        verbose_name = "قیمت محصول"
        verbose_name_plural = "قیمت محصولات"

    def __str__(self):
        return f"{self.product} - {self.final_price}"

    @property
    def final_price(self):
        return self.price - (self.price * self.discount_percent // 100)


class Product(models.Model):
    title = models.CharField("عنوان محصول", max_length=200)
    description = models.TextField("توضیحات", blank=True)
    category = models.ForeignKey(Category, verbose_name="دسته", on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, verbose_name="برند", on_delete=models.PROTECT, related_name="products")
    product_type = models.ForeignKey(
        ProductType, verbose_name="نوع محصول", on_delete=models.PROTECT, related_name="products"
    )
    attributes = models.ManyToManyField(ProductAttributeValue, verbose_name="ویژگی‌ها", related_name="products", blank=True)
    stock = models.PositiveIntegerField("موجودی", default=0)
    sold_count = models.PositiveIntegerField("تعداد فروش", default=0)
    is_active = models.BooleanField("فعال", default=True)
    base_image = models.ImageField("تصویر اصلی", upload_to="products/", null=True, blank=True)
    created_time = models.DateTimeField("زمان ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_time"]

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        return self.price.final_price if hasattr(self, "price") else None

    @property
    def discount_percent(self):
        return self.price.discount_percent if hasattr(self, "price") else 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("تصویر", upload_to="products/gallery/")

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self):
        return f"{self.product} #{self.pk}"


class Basket(models.Model):
    EXPIRED = 'expired'
    PENDING = 'pending'
    PAID = 'paid'
    STATUS_CHOICES = [
        (EXPIRED, 'منقضی'),
        (PENDING, 'در انتظار'),
        (PAID, 'پرداخت شده'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='baskets')
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
        ordering = ['-created_time']

    def __str__(self):
        return f'سبد {self.user} - {self.get_status_display()}'

    @property
    def total_price(self):
        total = 0
        for line in self.lines.all():
            total += line.line_total
        return total

    @property
    def total_items(self):
        return sum(line.quantity for line in self.lines.all())


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_lines')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'آیتم سبد'
        verbose_name_plural = 'آیتم‌های سبد'
        unique_together = [('basket', 'product')]

    def __str__(self):
        return f'{self.product} x {self.quantity}'

    @property
    def line_total(self):
        if hasattr(self.product, 'price'):
            return self.product.price.final_price * self.quantity
        return 0
