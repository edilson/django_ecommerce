from django.test import TestCase, Client
from django.urls import reverse

from users.models import User

class SignupViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')

    def test_signup_ok(self):
        data = {
            'username': 'edilson',
            'password1': 'python1!',
            'password2': 'python1!',
            'email': 'test@test.com',
        }
        response = self.client.post(self.signup_url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_error(self):
        data = {
            'username': 'edilson',
            'password1': 'python1!',
            'password2': 'python1!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
