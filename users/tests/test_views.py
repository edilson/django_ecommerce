from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from users.models import User
from users.tests.test_view_helper import *

class SignupViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')

    def test_signup_ok(self):
        data = {
            'username': 'test',
            'password1': 'python1!',
            'password2': 'python1!',
            'email': 'test@test.com',
        }
        response = self.client.post(self.signup_url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_without_data(self):
        data = {}
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, 'form', 'username', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'password1', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'password2', 'Este campo é obrigatório.')

    def test_signup_with_invalid_email(self):
        data = {
            'username': 'test',
            'email': 'testtest.com',
            'password1': 'python1!',
            'password2': 'python1!'
        }
        helper_test_signup_fields(self, data, 'email', 'Informe um endereço de email válido.')

    def test_signup_with_unmatching_passwords(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'python1!',
            'password2': 'pyth0n1'
        }
        helper_test_signup_fields(self, data, 'password2', 'The two password fields didn’t match.')

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

    def test_redirects_to_login_page_when_trying_to_access_the_update_user_page_without_sign_in(self):
        helper_test_redirect_to_login_page(self)

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

    def test_update_password_with_old_password_incorrect(self):
        data = {
            'old_password': '1234',
            'new_password1': 'pyth0n123',
            'new_password2': 'pyth0n123',
        }
        self.client.login(username=self.user.username, password='123')
        helper_test_update_fields(self, data, 'old_password', 'A senha antiga foi digitada incorretamente. Por favor, informe-a novamente.')

    def test_update_password_with_new_password_not_matching_at_confirmation(self):
        data = {
            'old_password': '123',
            'new_password1': 'pyth0n123',
            'new_password2': 'python123',
        }
        self.client.login(username=self.user.username, password='123')
        helper_test_update_fields(self, data, 'new_password2', 'The two password fields didn’t match.')

    def test_redirects_to_login_page_when_trying_to_access_the_update_password_page_without_sign_in(self):
        helper_test_redirect_to_login_page(self)
