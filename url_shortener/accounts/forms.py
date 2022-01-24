from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.fields import ReCaptchaV3

from .models import User


class UserRegisterForm(UserCreationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            attrs={
                'required_score': 0.85,
            },
        ),
        label=False
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget = forms.EmailInput()
