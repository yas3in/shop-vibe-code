from django.db import models


class Address(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='addresses')
    receipt_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    full_address = models.TextField()
    address_detail = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس‌ها'
        ordering = ['-is_default', '-created_time']

    def __str__(self):
        return f'{self.receipt_name} - {self.city}'
