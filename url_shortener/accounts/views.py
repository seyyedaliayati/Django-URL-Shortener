from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .forms import UserRegisterForm, UserLoginForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm


class CustomLogoutView(LogoutView):
    pass

class RegisterView(SuccessMessageMixin, CreateView):
  template_name = 'accounts/register.html'
  success_url = reverse_lazy('accounts:login')
  form_class = UserRegisterForm
  success_message = _("Your account was created successfully")
