import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    STATUS_CHOICE = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("canceled", "لغو شده"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    ref_id = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="pending", db_index=True)
    receipt_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=11)
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=10)
    full_address = models.TextField()
    address_detail = models.CharField(max_length=150, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"سفارش {self.ref_id} - {self.user}"

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="order_items",
    )
    product_title = models.CharField(max_length=200)
    unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_title} - {self.quantity}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity


class Payment(models.Model):
    STATUS_CHOICE = [
        ("pending", "در انتظار نتیجه"),
        ("success", "موفق"),
        ("failed", "ناموفق"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField()
    ref_id = models.CharField(max_length=40, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="pending")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پرداخت {self.ref_id} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.ref_id:
            self.ref_id = uuid.uuid4().hex[:14].upper()
        super().save(*args, **kwargs)
