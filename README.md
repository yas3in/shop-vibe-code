# AirShop — فروشگاه ایرپاد (Django / MVT)

پروژه دموی فروشگاه آنلاین ایرپاد با Django 5 و معماری MVT، فارسی و راست‌به‌چپ.

## اجرا

```bash
cd shop
source .venv/bin/activate
python manage.py migrate
python manage.py seed_demo      # داده‌های نمونه + کاربر ادمین
python manage.py runserver      # یا: .venv/bin/gunicorn config.wsgi --bind 0.0.0.0:8010
```

- سایت: http://127.0.0.1:8010
- ادمین جنگو: http://127.0.0.1:8010/admin/
- پنل محصولات: http://127.0.0.1:8010/panel/catalog/
- کاربر ادمین: `admin / admin123` — کاربر دمو: `demo / demo1234`

## ساختار

- `config/` — تنظیمات، urls اصلی، wsgi
- `core/` — صفحه اصلی (بنر، پرفروش، برندها، بیشترین تخفیف، درباره، خدمات)، تماس با ما
- `catalog/` — برند، دسته، نوع محصول، ویژگی‌ها، محصول، قیمت، تصاویر، سبد خرید (فرانت + پنل)
- `accounts/` — ثبت‌نام/ورود با Session، پروفایل
- `addresses/` — آدرس‌های کاربر
- `orders/` — سفارش، ردیف سفارش، پرداخت (درگاه فیک + کال‌بک)

ویوها/URLها/فرم‌های هر اپ به تفکیک فرانت و پنل در پوشه‌های `views/` و `urls/` و `forms/` هستند.

## پالت رنگی

- پس‌زمینه: `#1D4533` — اصلی: `#5E3122` — فرعی: `#F9D2BA` و `#F7EAE0`
- هدر گلی‌مورفیسم گرد با عرض ۱۳۰۰ پیکسل

## تست‌ها

```bash
python manage.py test core
```
