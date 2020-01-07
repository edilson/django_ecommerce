from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from catalog.models import Category, Product
from catalog.tests.test_model_helper import *

class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = mommy.make(Category)

    def test_get_absolute_url(self):
        helper_test_get_absolute_url(self, self.category, 'catalog:category')

    def test_ordering(self):
        helper_test_ordering(self, self.category, 'name')

class ProductTestCase(TestCase):
    def setUp(self):
        self.product = mommy.make(Product)

    def test_get_absolute_url(self):
        helper_test_get_absolute_url(self, self.product, 'catalog:product')

    def test_ordering(self):
        helper_test_ordering(self, self.product, 'name')
