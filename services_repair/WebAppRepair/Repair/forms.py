from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import *


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=True, initial=True,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                     label='Запомнить меня')
    captcha = CaptchaField(
        label='Подтвердите, что вы не робот',
        error_messages={'invalid': 'Неправильная капча, попробуйте еще раз'},
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

class RegistrForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Поле обязательное для заполнения')
    first_name = forms.CharField(required=True, label="Ваше имя", max_length=254)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2',)
