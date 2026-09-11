from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="کاربر", on_delete=models.CASCADE, related_name="addresses"
    )
    receipt_name = models.CharField("نام گیرنده", max_length=120)
    phone_number = models.CharField("شماره تماس", max_length=15)
    city = models.CharField("شهر", max_length=80)
    postal_code = models.CharField("کد پستی", max_length=12)
    full_address = models.TextField("آدرس کامل")
    address_detail = models.CharField("جزئیات آدرس (پلاک/واحد)", max_length=150, blank=True)
    is_default = models.BooleanField("پیش‌فرض", default=False)
    created_time = models.DateTimeField("زمان ایجاد", auto_now_add=True)
    updated_time = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
        ordering = ["-is_default", "-updated_time"]

    def __str__(self):
        return f"{self.user} - {self.city} - {self.receipt_name}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
