from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import UserAdminCreationForm

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'

class SignupView(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')

class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user

