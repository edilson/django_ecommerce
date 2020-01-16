from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from checkout.models import CartItem, Order, OrderItem

class CreateCartItemView(TestCase):
    def setUp(self):
        self.product = mommy.make('catalog.Product')
        self.client = Client()
        self.url = reverse('checkout:create_cartitem', kwargs={'slug': self.product.slug})

    def tearDown(self):
        self.product.delete()
        CartItem.objects.all().delete()

    def test_add_cart_item(self):
        response = self.client.get(self.url)
        redirect_url = reverse('checkout:cart_item')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_update_quantity_of_cart_item(self):
        response = self.client.get(self.url)
        response = self.client.get(self.url)
        cart_item = CartItem.objects.get()
        self.assertEqual(cart_item.quantity, 2)

class CheckoutViewTestCase(TestCase):
    def setUp(self):
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
        self.cart_item = mommy.make(CartItem)
        self.client = Client()
        self.checkout_url = reverse('checkout:checkout')

    def test_checkout_view(self):
        response_to_redirect = self.client.get(self.checkout_url)
        redirect_url = f'{reverse(settings.LOGIN_URL)}?next={self.checkout_url}'
        self.assertRedirects(response_to_redirect, redirect_url)
        self.client.login(username=self.user.username, password='123')
        self.cart_item.cart_id = self.client.session.session_key
        self.cart_item.save()
        response_with_cart_id = self.client.get(self.checkout_url)
        self.assertTemplateUsed(response_with_cart_id, 'checkout/checkout.html')

class OrderListViewTestCase(TestCase):
    def setUp(self):
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
        self.order_items = mommy.make(OrderItem, _quantity=9)
        self.orders = mommy.make(Order, _quantity=9)
        self.client = Client()
        self.url = reverse('checkout:order_list')
        self.response = self.client.get(self.url)

    def test_order_list_view(self):
        redirect_url = f'{reverse(settings.LOGIN_URL)}?next={self.url}'
        self.assertRedirects(self.response, redirect_url)
        self.client.login(username=self.user.username, password='123')
        response_logged_in = self.client.get(self.url)
        self.assertTemplateUsed(response_logged_in, 'checkout/order_list.html')

