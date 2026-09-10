import uuid
from django.db import models


class Order(models.Model):
    PENDING = 'pending'
    PAID = 'paid'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'در انتظار پرداخت'),
        (PAID, 'پرداخت شده'),
        (CANCELLED, 'لغو شده'),
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey('addresses.Address', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.PositiveIntegerField(default=0)
    tracking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_time']

    def __str__(self):
        return f'سفارش {self.tracking_code}'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey('catalog.Product', on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f'{self.product_title} x {self.quantity}'

    @property
    def line_total(self):
        return self.price * self.quantity


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.PositiveIntegerField(default=0)
    transaction_id = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'

    def __str__(self):
        return f'پرداخت سفارش {self.order.tracking_code}'
