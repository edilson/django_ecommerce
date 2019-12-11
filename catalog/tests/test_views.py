from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from catalog.models import Product, Category

class ProductListTestCase(TestCase):
    def setUp(self):
        self.url = reverse('catalog:product_list')
        self.client = Client()
        self.products = mommy.make(Product, _quantity=3)
        self.response = self.client.get(self.url)

    def tearDown(self):
        Product.objects.all().delete()

    def test_view_ok(self):
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'catalog/product_list.html')

    def test_context(self):
        self.assertTrue('product_list' in self.response.context)
        product_list = self.response.context['product_list']
        self.assertEquals(product_list.count(), 3)
