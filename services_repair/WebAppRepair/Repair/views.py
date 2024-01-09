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
    action = Stock.objects.all()
    user_photo = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        captcha = request.POST.get('captcha')
        user = authenticate(request, username=username, password=password, captcha=captcha)

        if user:
            login(request, user)

            if remember_me == 'on':
                request.session.set_expiry(1209600)

            return redirect('profile')
        else:
            return render(request, 'home/home.html', {'error_message': 'Неправильные учетные данные'})
    else:
        form = CustomAuthenticationForm()

    if request.user.is_authenticated:
        user_photo = request.user.image

    objects_count = len(action)
    third = objects_count // 3

    first_column = action[2*third:]
    second_column = action[third:2*third]
    third_column = action[:third]
    context = {
        "form": form,
        "first_column": first_column,
        "second_column": second_column,
        "third_column": third_column,
        "user_photo": user_photo,
    }

    return render(request, "home/home.html", context)



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

def services_materials(request):

    latest_price_list_services = Price_list_services.objects.latest('date')
    latest_positions_services = Price_list_services_pozition.objects.filter(price_list=latest_price_list_services)


    services_count = len(latest_positions_services)
    third_services = services_count // 3

    first_column_services = latest_positions_services[:third_services]
    second_column_services = latest_positions_services[third_services:2 * third_services]
    third_column_services = latest_positions_services[2 * third_services:]

    latest_price_list_materials= Price_list_material.objects.latest('date')
    latest_positions_materials = Price_list_material_pozition.objects.filter(price_list=latest_price_list_materials).filter(material__type_material='Ателье')

    materials_count = len(latest_positions_materials)
    third_materials = materials_count // 3

    first_column_materials = latest_positions_materials[2*third_materials:]
    second_column_materials = latest_positions_materials[third_materials:2 * third_materials]
    third_column_materials = latest_positions_materials[:third_materials]

    context = {
        "first_column_services": first_column_services,
        "second_column_services": second_column_services,
        "third_column_services": third_column_services,
        "first_column_materials": first_column_materials,
        "second_column_materials": second_column_materials,
        "third_column_materials": third_column_materials,
    }

    return render(request, "services_materials.html", context)