from django.contrib.auth.models import User
from django.test import Client, TestCase

from addresses.models import Address
from catalog.models import Basket, Product
from orders.models import Order, Payment


class ShopFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("demo", "demo@x.com", "demo1234")
        from catalog.models import Brand, Category, ProductPrice, ProductType

        brand = Brand.objects.create(name="Apple")
        category = Category.objects.create(name="ایرپاد", slug="irpad")
        ptype = ProductType.objects.create(title="ایرپاد")
        self.product = Product.objects.create(
            title="ایرپاد تست", category=category, brand=brand, product_type=ptype, stock=10, is_active=True
        )
        ProductPrice.objects.create(product=self.product, price=1000000, discount_percent=10)
        self.address = Address.objects.create(
            user=self.user, receipt_name="دمو", phone_number="0912", city="تهران",
            postal_code="1", full_address="آدرس تست", is_default=True,
        )

    def test_public_pages(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/catalog/").status_code, 200)
        self.assertEqual(self.client.get(f"/catalog/{self.product.pk}/").status_code, 200)
        self.assertEqual(self.client.get("/contact/").status_code, 200)

    def test_login_and_basket_flow(self):
        self.assertTrue(self.client.login(username="demo", password="demo1234"))
        self.client.post(f"/orders/basket/add/{self.product.pk}/")
        self.assertEqual(self.client.get("/orders/basket/").status_code, 200)

        response = self.client.post("/orders/checkout/", {"address_id": self.address.pk})
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.items.count(), 1)
        self.assertRedirects(response, f"/payments/gateway/{order.pk}/", fetch_redirect_response=False)

        self.assertEqual(self.client.get(f"/payments/gateway/{order.pk}/").status_code, 200)
        self.client.post(f"/payments/callback/{order.pk}/")
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)
        payment = Payment.objects.get(order=order)
        self.assertEqual(payment.status, Payment.Status.SUCCESS)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)
        self.assertEqual(self.product.sold_count, 1)

    def test_register(self):
        response = self.client.post(
            "/accounts/register/",
            {"username": "newuser", "email": "n@x.com", "password1": "pass12345", "password2": "pass12345"},
        )
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertEqual(response.status_code, 302)

    def test_admin_panel(self):
        User.objects.create_superuser("admin", "a@x.com", "admin123")
        admin_client = Client()
        admin_client.login(username="admin", password="admin123")
        self.assertEqual(admin_client.get("/panel/catalog/products/").status_code, 200)
        self.assertEqual(admin_client.get("/panel/catalog/products/create/").status_code, 200)
        self.assertEqual(admin_client.get("/admin/").status_code, 200)
