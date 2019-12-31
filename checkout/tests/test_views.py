from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from checkout.models import CartItem

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

