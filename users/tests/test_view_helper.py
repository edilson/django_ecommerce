from django.urls import reverse
from django.conf import settings

def helper_test_signup_fields(instance_tested, data, field, form_message):
    response = instance_tested.client.post(instance_tested.signup_url, data)
    instance_tested.assertFormError(response, 'form', field, form_message)

def helper_test_update_fields(instance_tested, data, field, form_message):
    response = instance_tested.client.post(instance_tested.url, data)
    instance_tested.user.refresh_from_db()
    instance_tested.assertFormError(response, 'form', field, form_message)

def helper_test_redirect_to_login_page(instance_tested):
    response = instance_tested.client.get(instance_tested.url)
    redirect_url = f'{reverse(settings.LOGIN_URL)}?next={instance_tested.url}'
    instance_tested.assertEqual(response.status_code, 302)
    instance_tested.assertRedirects(response, redirect_url)
