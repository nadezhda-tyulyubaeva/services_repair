from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

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
    last_name = forms.CharField(required=True, label='Ваша фамилия')
    middle_name = forms.CharField(required=True, label='Ваше отчество')
    email = forms.EmailField(max_length=254, help_text='Поле обязательное для заполнения')
    first_name = forms.CharField(required=True, label="Ваше имя", max_length=254)
    agree = forms.BooleanField(label=' ', help_text='В соответствии с Федеральным законом от 27.06.2006 № 152-ФЗ "О персональных данных" даю согласие на обработку персональных данных')

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'middle_name', 'email', 'number', 'username',  'password1', 'password2', 'agree', )

class OrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ('number', 'client', 'date', 'NDS', 'actual_production_date', 'planned_production_date', 'product',)
