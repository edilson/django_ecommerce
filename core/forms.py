from django import forms
from django.core.mail import send_mail
from django_ecommerce.settings import local_base

class ContactForm(forms.Form):
    name = forms.CharField(label='Nome', required=True)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        message = f'Nome:{name}\nEmail:{email}\n{message}'
        send_mail('Contato do Django E-commerce', message, local_base.DEFAULT_FROM_EMAIL, [local_base.DEFAULT_FROM_EMAIL])
