from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from catalog.models import Product, Category, Brand, ProductType, ProductPrice, Basket, BasketLine
from addresses.models import Address
from orders.models import Order, OrderLine, Payment


class AirShopFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='ایرپاد پرو', slug='pro')
        self.brand = Brand.objects.create(name='Apple')
        self.ptype = ProductType.objects.create(title='ایرپاد')
        self.product = Product.objects.create(
            title='ایرپاد تست',
            description='توضیحات تست',
            category=self.category,
            brand=self.brand,
            product_type=self.ptype,
            stock=10,
            is_active=True
        )
        self.price = ProductPrice.objects.create(product=self.product, price=10000000, discount_percent=10)
        self.address = Address.objects.create(
            user=self.user,
            receipt_name='کاربر تست',
            phone_number='09120000000',
            city='تهران',
            postal_code='1111111111',
            full_address='تهران خیابان تست',
            is_default=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AirShop')
        self.assertContains(response, 'ایرپاد تست')

    def test_product_list_and_detail(self):
        list_resp = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, 'ایرپاد تست')

        detail_resp = self.client.get(reverse('catalog:product_detail', args=[self.product.pk]))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, 'ایرپاد تست')

    def test_contact_page(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_full_checkout_and_payment_flow(self):
        self.client.login(username='testuser', password='password123')

        add_resp = self.client.get(reverse('orders:basket_add', args=[self.product.pk]))
        self.assertEqual(add_resp.status_code, 302)

        basket_resp = self.client.get(reverse('orders:basket'))
        self.assertEqual(basket_resp.status_code, 200)
        self.assertContains(basket_resp, 'ایرپاد تست')

        checkout_resp = self.client.post(reverse('orders:checkout_address'), {'address_id': self.address.pk})
        self.assertEqual(checkout_resp.status_code, 302)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 9000000)

        gateway_resp = self.client.get(reverse('orders:payment_gateway', args=[order.pk]))
        self.assertEqual(gateway_resp.status_code, 200)

        callback_resp = self.client.post(reverse('orders:payment_callback', args=[order.pk]))
        self.assertEqual(callback_resp.status_code, 302)

        order.refresh_from_db()
        self.assertEqual(order.status, Order.PAID)
        self.assertTrue(order.payment.is_paid)

        detail_resp = self.client.get(reverse('orders:order_detail', args=[order.pk]))
        self.assertEqual(detail_resp.status_code, 200)
        self.assertContains(detail_resp, 'پرداخت شده')
