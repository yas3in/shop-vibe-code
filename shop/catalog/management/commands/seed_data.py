import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from catalog.models import (
    Brand, Category, ProductType, ProductAttribute,
    ProductAttributeValue, Product, ProductPrice, ProductImage
)
from addresses.models import Address


def create_placeholder_image(text, color, width=600, height=600):
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(249, 210, 186), width=3)
    draw.text((width // 2 - 80, height // 2 - 10), text, fill=(247, 234, 224))
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=90)
    return ContentFile(buffer.getvalue(), name=f"{text}.jpg")


class Command(BaseCommand):
    help = 'Seeds database with initial demo data for AirShop'

    def handle(self, *args, **kwargs):
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@airshop.ir'})
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        demo_user, _ = User.objects.get_or_create(username='user', defaults={'email': 'user@airshop.ir'})
        demo_user.set_password('user123')
        demo_user.save()

        Address.objects.get_or_create(
            user=demo_user,
            receipt_name='علی رضایی',
            phone_number='09123456789',
            city='تهران',
            postal_code='1234567890',
            full_address='خیابان ولیعصر، بالاتر از میدان ونک، کوچه شادمان، پلاک ۱۲',
            address_detail='واحد ۴، زنگ ۴',
            is_default=True
        )

        cat_pro, _ = Category.objects.get_or_create(name='ایرپاد پرو', slug='airpods-pro')
        cat_max, _ = Category.objects.get_or_create(name='ایرپاد مکس', slug='airpods-max')
        cat_std, _ = Category.objects.get_or_create(name='ایرپاد استاندارد', slug='airpods-standard')
        cat_acc, _ = Category.objects.get_or_create(name='لوازم جانبی صوتی', slug='audio-accessories')

        brand_apple, _ = Brand.objects.get_or_create(name='Apple')
        brand_samsung, _ = Brand.objects.get_or_create(name='Samsung')
        brand_sony, _ = Brand.objects.get_or_create(name='Sony')
        brand_anker, _ = Brand.objects.get_or_create(name='Anker')
        brand_jbl, _ = Brand.objects.get_or_create(name='JBL')

        ptype, _ = ProductType.objects.get_or_create(title='هدفون و ایرپاد بی‌سیم')

        attr_anc, _ = ProductAttribute.objects.get_or_create(product_type=ptype, name='قابلیت نویز کنسلینگ (ANC)')
        attr_bt, _ = ProductAttribute.objects.get_or_create(product_type=ptype, name='نسخه بلوتوث')
        attr_battery, _ = ProductAttribute.objects.get_or_create(product_type=ptype, name='شارژدهی باتری')
        attr_water, _ = ProductAttribute.objects.get_or_create(product_type=ptype, name='مقاومت در برابر آب')

        val_anc_yes, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_anc, value='دارد (فعال)')
        val_anc_no, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_anc, value='ندارد')
        val_bt53, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_bt, value='Bluetooth 5.3')
        val_bt52, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_bt, value='Bluetooth 5.2')
        val_bat30, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_battery, value='تا ۳۰ ساعت همراه با کیس')
        val_bat24, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_battery, value='تا ۲۴ ساعت همراه با کیس')
        val_ipx4, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_water, value='IPX4')
        val_ipx7, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_water, value='IPX7')

        products_data = [
            {
                'title': 'اپل ایرپاد پرو ۲ با پورت تایپ سی (Apple AirPods Pro 2 Type-C)',
                'category': cat_pro,
                'brand': brand_apple,
                'price': 13500000,
                'discount': 12,
                'stock': 25,
                'sold': 85,
                'desc': 'نسل دوم ایرپاد پرو با چیپست قدرتمند H2، نویز کنسلینگ فعال تا ۲ برابر قوی‌تر و شارژدهی تا ۳۰ ساعت با کیس شارژ مجهز به درگاه USB-C.',
                'color': (94, 49, 34),
                'attrs': [val_anc_yes, val_bt53, val_bat30, val_ipx4]
            },
            {
                'title': 'اپل ایرپاد مکس (Apple AirPods Max)',
                'category': cat_max,
                'brand': brand_apple,
                'price': 34000000,
                'discount': 15,
                'stock': 8,
                'sold': 32,
                'desc': 'هدفون روگوشی بی‌نظیر اپل با کیفیت صدای های‌فای، درایورهای داینامیک اختصاصی و نویز کنسلینگ پیشرفته برای تجربه صوتی سینمایی.',
                'color': (45, 30, 25),
                'attrs': [val_anc_yes, val_bt52, val_bat24, val_ipx4]
            },
            {
                'title': 'اپل ایرپاد ۳ (Apple AirPods 3rd Gen)',
                'category': cat_std,
                'brand': brand_apple,
                'price': 9800000,
                'discount': 5,
                'stock': 30,
                'sold': 95,
                'desc': 'طراحی جدید و ارگونومیک با پشتیبانی از Spatial Audio و رهگیری پویای حرکات سر همراه با مقاومت در برابر تعریق و قطرات آب.',
                'color': (70, 40, 30),
                'attrs': [val_anc_no, val_bt53, val_bat30, val_ipx4]
            },
            {
                'title': 'سامسونگ گلکسی بادز ۲ پرو (Samsung Galaxy Buds 2 Pro)',
                'category': cat_pro,
                'brand': brand_samsung,
                'price': 7200000,
                'discount': 20,
                'stock': 20,
                'sold': 64,
                'desc': 'صدای با کیفیت ۲۴ بیتی Hi-Fi، طراحی کوچک‌تر و راحت‌تر، و حذف نویز فعال هوشمند برای مکالمات شفاف و موسیقی زنده.',
                'color': (30, 50, 40),
                'attrs': [val_anc_yes, val_bt53, val_bat24, val_ipx7]
            },
            {
                'title': 'سونی WF-1000XM5 (Sony WF-1000XM5 Wireless Earbuds)',
                'category': cat_pro,
                'brand': brand_sony,
                'price': 15200000,
                'discount': 8,
                'stock': 12,
                'sold': 47,
                'desc': 'بهترین سیستم حذف نویز جهان با دو پردازنده اختصاصی، کیفیت صدای ممتاز و میکروفون‌های هدایت صوتی استخوان برای بالاترین کیفیت مکالمه.',
                'color': (25, 45, 35),
                'attrs': [val_anc_yes, val_bt53, val_bat24, val_ipx4]
            },
            {
                'title': 'انکر ساندکور لیبرتی ۴ (Anker Soundcore Liberty 4 NC)',
                'category': cat_std,
                'brand': brand_anker,
                'price': 4800000,
                'discount': 25,
                'stock': 40,
                'sold': 120,
                'desc': 'کاهش نویز تا ۹۸.۵ درصد، درایورهای کاستوم ۱۱ میلی‌متری و گواهی صوتی Hi-Res Wireless با عمر باتری فوق‌العاده تا ۵۰ ساعت.',
                'color': (80, 45, 35),
                'attrs': [val_anc_yes, val_bt53, val_bat30, val_ipx4]
            },
            {
                'title': 'جی‌بی‌ال Tune 230NC TWS (JBL Tune 230NC)',
                'category': cat_std,
                'brand': brand_jbl,
                'price': 3900000,
                'discount': 18,
                'stock': 18,
                'sold': 58,
                'desc': 'بیس خالص JBL Pure Bass Sound با ۴ میکروفون برای مکالمه بدون نویز و باتری با شارژدهی تا ۴۰ ساعت.',
                'color': (60, 35, 25),
                'attrs': [val_anc_yes, val_bt52, val_bat30, val_ipx4]
            },
            {
                'title': 'سامسونگ گلکسی بادز اف‌ای (Samsung Galaxy Buds FE)',
                'category': cat_std,
                'brand': brand_samsung,
                'price': 3400000,
                'discount': 15,
                'stock': 22,
                'sold': 72,
                'desc': 'طراحی جمع‌وجور و سبک با بالشتک‌های سیلیکونی، نویز کنسلینگ فعال کارآمد و ارگونومی فوق‌العاده برای استفاده روزمره.',
                'color': (40, 55, 45),
                'attrs': [val_anc_yes, val_bt52, val_bat30, val_ipx4]
            }
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                title=p_data['title'],
                defaults={
                    'description': p_data['desc'],
                    'category': p_data['category'],
                    'brand': p_data['brand'],
                    'product_type': ptype,
                    'stock': p_data['stock'],
                    'sold_count': p_data['sold'],
                    'is_active': True,
                }
            )
            if created:
                img_file = create_placeholder_image(p_data['brand'].name, p_data['color'])
                product.base_image.save(f"{product.pk}.jpg", img_file, save=True)

                ProductPrice.objects.create(
                    product=product,
                    price=p_data['price'],
                    discount_percent=p_data['discount']
                )

                for attr_val in p_data['attrs']:
                    product.attributes.add(attr_val)

        self.stdout.write(self.style.SUCCESS('Successfully seeded AirShop database with demo data!'))
