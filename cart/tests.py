from django.test import TestCase
from django.urls import reverse
from core.models import Category, Product


class CartQuantityTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='TVs', slug='tvs')
        self.product = Product.objects.create(
            name='Smart TV 32 Inch',
            slug='smart-tv-32',
            description='32 inch smart tv',
            price=15000.00,
            category=self.category,
            stock=50
        )

    def test_add_to_cart_default_quantity(self):
        url = reverse('add_to_cart', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cart_session = self.client.session.get('cart', {})
        self.assertEqual(cart_session.get(str(self.product.id)), 1)

    def test_add_to_cart_custom_quantity(self):
        url = reverse('add_to_cart', kwargs={'product_id': self.product.id})
        response = self.client.post(url, {'quantity': 15})
        self.assertEqual(response.status_code, 302)
        cart_session = self.client.session.get('cart', {})
        self.assertEqual(cart_session.get(str(self.product.id)), 15)

    def test_add_to_cart_bounded_by_stock(self):
        url = reverse('add_to_cart', kwargs={'product_id': self.product.id})
        response = self.client.post(url, {'quantity': 100})  # stock is 50
        self.assertEqual(response.status_code, 302)
        cart_session = self.client.session.get('cart', {})
        self.assertEqual(cart_session.get(str(self.product.id)), 50)

