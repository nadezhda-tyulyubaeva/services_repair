from os import name

from django.shortcuts import render, redirect, get_object_or_404
from .models import *

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, RegistrForm
from django.contrib.auth import authenticate, login

import logging

logger = logging.getLogger(name)

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        captcha = request.POST.get('captcha')
        user = authenticate(request, username=username, password=password, captcha=captcha)

        if user:
            login(request, user)
            # Проверяем remember_me
            if remember_me == 'on':
                request.session.set_expiry(1209600)  # Например, устанавливаем срок действия сессии на 2 недели

            # После успешной аутентификации, перенаправляем на нужную страницу
            return redirect('profile')  # Замените 'profile' на ваш URL для профиля пользователя
        else:
            # Обработка неправильной аутентификации: вывод сообщения об ошибке или перенаправление на страницу снова
            return render(request, 'home/home.html', {'error_message': 'Неправильные учетные данные'})
    else:
        form = CustomAuthenticationForm()

    return render(request, "home/home.html", {"form": form})


def registrat(request):
    data = {}

    if request.method == 'POST':

        form = RegistrForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            data['form'] = form

            return render(request, 'registration/registration_out.html', data)

    else:
        form = RegistrForm()
        data['form'] = form
    return render(request, 'registration/registration.html', data)
# Create your views here.

def profiles(request):
    # Проверка, является ли пользователь аутентифицированным
    if request.user.is_authenticated:
        # Получение профиля текущего аутентифицированного пользователя
        profile = get_object_or_404(CustomUser, pk=request.user.pk)
        context = {'my_profile': profile}
        return render(request, 'profile.html', context)
    else:
        # Дополнительные действия, если пользователь не аутентифицирован
        # Например, перенаправление на страницу входа или вывод сообщения об ошибке
        return render(request, 'not_authenticated.html')