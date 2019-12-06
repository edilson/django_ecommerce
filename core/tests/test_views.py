from django.test import TestCase, Client
from django.urls import reverse

class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.response = self.client.get(self.url)

    def tearDown(self):
        pass

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'index.html')