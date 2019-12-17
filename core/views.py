from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from catalog.models import Category
from core.forms import ContactForm

User = get_user_model()

class IndexView(TemplateView):

    template_name = 'index.html'

def contact(request):
    success = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    model = User
    success_url = reverse_lazy('index')
