import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from catalog.models import (
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductPrice,
    ProductType,
)

BRANDS = ["Apple", "Samsung", "Xiaomi", "Anker", "Sony", "JBL"]
CATEGORIES = [
    ("ایرپاد", None),
    ("هندزفری", "ایرپاد"),
    ("هدفون", None),
    ("اسپیکر", None),
]
PRODUCTS = [
    ("ایرپاد اپل AirPods Pro 2", "Apple", "ایرپاد", 8900000, 15),
    ("ایرپاد اپل AirPods 3", "Apple", "ایرپاد", 6200000, 0),
    ("گلکسی بادز Samsung Buds2 Pro", "Samsung", "ایرپاد", 5400000, 20),
    ("ردمی بادز Xiaomi Redmi Buds 4", "Xiaomi", "هندزفری", 1450000, 10),
    ("انکر ساندکور Anker Soundcore P20i", "Anker", "هندزفری", 990000, 25),
    ("سونی WF-C500", "Sony", "ایرپاد", 3100000, 5),
    ("جی بی ال JBL Tune 130NC", "JBL", "هدفون", 2700000, 12),
    ("هدفون سونی WH-1000XM5", "Sony", "هدفون", 14500000, 8),
    ("اسپیکر جی بی ال JBL Flip 6", "JBL", "اسپیکر", 4300000, 18),
    ("اسپیکر انکر Anker Soundcore 3", "Anker", "اسپیکر", 2100000, 0),
    ("ایرپاد اپل AirPods Max", "Apple", "هدفون", 18900000, 30),
    ("گلکسی بادز فئ Samsung Buds FE", "Samsung", "ایرپاد", 1900000, 22),
]


class Command(BaseCommand):
    help = "ساخت داده‌های نمونه فروشگاه"

    def handle(self, *args, **options):
        brands = {}
        for name in BRANDS:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands[name] = brand

        categories = {}
        for name, parent in CATEGORIES:
            category, _ = Category.objects.get_or_create(
                name=name, parent=categories.get(parent) if parent else None,
                defaults={"slug": name.replace(" ", "-")},
            )
            categories[name] = category

        ptype, _ = ProductType.objects.get_or_create(
            title="ایرپاد و تجهیزات صوتی", defaults={"description": "انواع ایرپاد، هدفون و اسپیکر"}
        )

        attr_specs = [
            ("اتصال", ["بلوتوث 5.3", "بلوتوث 5.2", "بلوتوث 5.0", "کابلی"]),
            ("زمان پخش", ["تا ۶ ساعت", "تا ۳۰ ساعت", "تا ۲۴ ساعت"]),
            ("ضد آب", ["IPX4", "IPX5", "ندارد"]),
        ]
        attrs = {}
        for attr_name, _ in attr_specs:
            attribute, _ = ProductAttribute.objects.get_or_create(product_type=ptype, name=attr_name)
            attrs[attr_name] = attribute

        for title, brand_name, cat_name, price, discount in PRODUCTS:
            product, created = Product.objects.get_or_create(
                title=title,
                defaults={
                    "description": f"{title} با کیفیت ساخت عالی و گارانتی معتبر.",
                    "category": categories[cat_name],
                    "brand": brands[brand_name],
                    "product_type": ptype,
                    "stock": random.randint(3, 25),
                    "sold_count": random.randint(0, 400),
                    "is_active": True,
                },
            )
            if created:
                product.price = ProductPrice.objects.create(
                    product=product, price=price, discount_percent=discount
                )
            if not product.attribute_values.exists():
                for attr_name, values in attr_specs:
                    for v in random.sample(values, random.randint(1, 2)):
                        ProductAttributeValue.objects.create(
                            product=product, product_attribute=attrs[attr_name], value=v
                        )

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@airshop.ir", "admin123")
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user("demo", "demo@airshop.ir", "demo1234")

        self.stdout.write(self.style.SUCCESS("داده‌های نمونه ساخته شد (admin/admin123 و demo/demo1234)"))
