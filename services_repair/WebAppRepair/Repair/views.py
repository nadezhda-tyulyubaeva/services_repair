import decimal
from os import name
from time import timezone

from django.db.models import OuterRef, Subquery, Max, F
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle, Table, SimpleDocTemplate, Paragraph, Spacer

from .models import *

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, RegistrForm, OrderCreateForm
from django.contrib.auth import authenticate, login

from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape

import logging

from datetime import datetime

import openpyxl
from django.http import HttpResponse

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

    first_column = action[2 * third:]
    second_column = action[third:2 * third]
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
    materials = Material_characteristics.objects.filter(material__description='Ткань для шитья и рукоделия Атлас стрейч, отрез 150 см * 200 см цвет сиреневый')

    latest_price_list_services = Price_list_services.objects.latest('date')
    latest_positions_services = Price_list_services_pozition.objects.filter(price_list=latest_price_list_services)

    services_count = len(latest_positions_services)
    third_services = services_count // 3

    first_column_services = latest_positions_services[:third_services]
    second_column_services = latest_positions_services[third_services:2 * third_services]
    third_column_services = latest_positions_services[2 * third_services:]

    latest_price_list_materials = Price_list_material.objects.latest('date')
    latest_positions_materials = Price_list_material_pozition.objects.filter(
        price_list=latest_price_list_materials).filter(material__type_material='Ателье')

    materials_count = len(latest_positions_materials)
    third_materials = materials_count // 3

    first_column_materials = latest_positions_materials[2 * third_materials:]
    second_column_materials = latest_positions_materials[third_materials:2 * third_materials]
    third_column_materials = latest_positions_materials[:third_materials]



    context = {
        'materials': materials,
        "first_column_services": first_column_services,
        "second_column_services": second_column_services,
        "third_column_services": third_column_services,
        "first_column_materials": first_column_materials,
        "second_column_materials": second_column_materials,
        "third_column_materials": third_column_materials,
    }

    return render(request, "services_materials.html", context)

def sale_of_materials(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Получение объектов за выбранный период
                materials_r = Materials_order.objects.filter(order__date__range=[start_date, end_date])
                if request.GET.get('export_excel'):
                    response = HttpResponse(content_type='application/ms-excel')
                    response['Content-Disposition'] = 'attachment; filename="report_sale_materials.xlsx"'

                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active
                    worksheet.title = 'Sales Report'
                    worksheet.append(['Дата', 'Наименование материала', 'Описание материала', 'Продано', 'Единицы измерения'])
                    for material in materials_r:
                        worksheet.append([material.order.date, material.pozition.material.name, material.pozition.material.description, material.count, material.unit_of_measurement.short_name])

                    workbook.save(response)
                    return response

                if request.GET.get('export_pdf'):
                    # Создание буфера для PDF
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="report_sale_of_materials.pdf"'

                    buffer = BytesIO()

                    # Создание PDF
                    p = SimpleDocTemplate(buffer, pagesize=landscape(letter))
                    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

                    styles = getSampleStyleSheet()
                    style_header = styles['Heading1']
                    style_header.fontName = 'Arial'
                    style_header.alignment = 1

                    style_normal = styles['Normal']
                    style_normal.fontSize = 12
                    style_normal.fontName = 'Arial'


                    data = [['Дата', 'Материал', 'Описание материала', 'Продано', 'Ед.', 'Цена, руб.']]

                    for material in materials_r:
                        data.append([
                            material.order.date,
                            material.pozition.material.name,
                            material.pozition.material.description,
                            material.count,
                            material.unit_of_measurement.short_name,
                            material.pozition.cost,
                        ])

                    table = Table(data)

                    style_table = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ])
                    table.setStyle(style_table)

                    elements = []
                    elements.append(Paragraph("Отчёт по продаже материалов", style_header))
                    elements.append(Spacer(1,12))
                    elements.append(table)
                    elements.append(Spacer(1, 12))
                    user_info = f"Администратор ______________________ {request.user.last_name} {request.user.first_name[0]}. {request.user.middle_name[0]}."
                    elements.append(Paragraph(user_info,  style_normal))
                    elements.append(Spacer(1, 12))
                    elements.append(Paragraph('_____________________________________________________________________________________________', style_normal))
                    elements.append(Spacer(1, 18))
                    period_info = f'Отчет сформирован за период с {start_date} по {end_date}'
                    elements.append(Paragraph(period_info, style_normal))
                    p.build(elements)

                    pdf = buffer.getvalue()
                    buffer.close()
                    response.write(pdf)

                    return response

                else:
                    context = {
                        'materials_r': materials_r,
                        'start_date': start_date,
                        'end_date': end_date,
                    }

                    return render(request, 'report/sale_of_materials.html', context)


            except ValueError:
                error_message = 'Дата указана неверно, используйте формат YYYY-MM-DD'
                return render(request, 'report/sale_of_materials.html', {'error_message': error_message})

        else:
            error_message = 'Укажите начальную и конечную дату'
            return render(request, 'report/sale_of_materials.html', {'error_message': error_message})

def daily_report(request):
    if request.method == 'GET':
        day_str = request.GET.get('day')

        if day_str:
            try:
                day = datetime.strptime(day_str, '%Y-%m-%d').date()

                # Получение объектов за выбранный период
                services = Order_pozition.objects.filter(order__date=day)
                materials = Materials_order.objects.filter(order__date=day)
                orders = Order.objects.filter(date=day)

                total_cost = 0
                total_cost_discount = 0
                total_cost_materials = 0
                total = 0
                total_discount = 0

                for service in services:
                    total_cost += service.service.cost
                    total_cost_discount += service.total_order_cost_with_discount
                for material in materials:
                    total_cost_materials += material.total_cost
                for order in orders:
                    total_cost_services = sum(service.service.cost for service in services.filter(order=order))
                    total_cost_materials_order = sum(material.total_cost for material in materials.filter(order=order))
                    total_cost_order = total_cost_services + total_cost_materials_order
                    order.total_cost = total_cost_order
                    if order.client.discount:
                        order.total_cost_discount = total_cost_order-(total_cost_order * order.client.discount / decimal.Decimal(str(100)))
                    else:
                        order.total_cost_discount = total_cost_order
                    total += order.total_cost
                    total_discount += order.total_cost_discount

                context = {
                    'services': services,
                    'materials': materials,
                    'orders': orders,
                    'day': day,
                    'total_cost': total_cost,
                    'total_cost_discount': total_cost_discount,
                    'total_cost_materials': total_cost_materials,
                    'total': total,
                    'total_discount': total_discount,

                }

                return render(request, 'report/daily_report.html', context)


            except ValueError:
                error_message = 'Дата указана неверно, используйте формат YYYY-MM-DD'
                return render(request, 'report/daily_report.html', {'error_message': error_message})

        else:
            error_message = 'Укажите дату'
            return render(request, 'report/daily_report.html', {'error_message': error_message})

class LoanedOrderAllListView(generic.ListView):
    model = Order
    template_name = 'orders/all_orders.html'
    context_object_name = 'all_orders'

    def get_queryset(self):
        # Подзапрос для получения последнего статуса каждого заказа
        latest_status_subquery = Order_status.objects.filter(
            order=OuterRef('pk')
        ).order_by('-date').values('order_status__name')[:1]

        # Основной запрос, возвращающий заказы с последним статусом
        queryset = Order.objects.annotate(
            latest_status=Subquery(latest_status_subquery)
        ).filter(
            latest_status__isnull=False
        ).order_by('latest_status', 'date')

        return queryset

def order_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query')

        if search_query is not None:


            # Проверяем, что query не None
            found_orders = Order_status.objects.filter(order__number__icontains=search_query)
            found_orders_latest_status = found_orders.annotate(
                latest_status=Max('date')
            ).filter(date=F('latest_status'))

            context = {
                'found_orders': found_orders_latest_status,
            }
            return render(request, 'orders/order_search.html', context)
        else:
            # Если query None, вернуть пустой результат или другое сообщение об ошибке
            return render(request, 'orders/order_search.html')

def create_order(request):
    if request.method == 'POST':
        orders = Order.objects.last()
        if orders:
            new_order = int(orders.number) + 1
        else:
            new_order = 1
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            neworder = Order.objects.create(
                number=new_order,
                client = form.cleaned_data['client'],


            )
            neworder.save()
            success_message = 'Заказ успешно оформлен.'
            return render(request, 'orders/create_order.html', {'success_message': success_message})
        else:
            print(form.errors)
    else:
        form = OrderCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'orders/create_order.html', context=context)
