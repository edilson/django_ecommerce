from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

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

class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_user_ok(self):
        data = {'name': 'test', 'email': 'test@test.com'}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        accounts_index_url = reverse('accounts:index')
        self.assertRedirects(response, accounts_index_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.name, 'test')

    def test_update_user_error(self):
        data = {}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')

class UpdatePasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_password_ok(self):
        data = {
            'old_password': '123',
            'new_password1': 'python1!',
            'new_password2': 'python1!',
        }
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('python1!'))

