from django.test import TestCase
from model_mommy import mommy

from checkout.models import CartItem, CartItemManager

class CartItemTestCase(TestCase):
    def setUp(self):
        self.cart_item = mommy.make(CartItem, _quantity=3)

    def test_post_save_cart_item(self):
        cart_item = CartItem.objects.all()[0]
        cart_item.quantity = 0
        cart_item.save()
        self.assertEqual(CartItem.objects.count(), 2)

    def test_cart_item_is_unique(self):
       unique_together = self.cart_item[0]._meta.unique_together
       self.assertEqual(unique_together[0], ('cart_id', 'product'))
