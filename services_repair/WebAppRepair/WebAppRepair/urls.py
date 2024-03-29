"""
URL configuration for WebAppRepair project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Repair.views import *
from django.urls import include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('registr/', registrat),

    path('profile/', profiles, name='profile'),

    path('captcha/', include('captcha.urls')),

    path('services_materials/', services_materials, name='services_materials'),

    path('sale_of_materials/', sale_of_materials, name='sale_of_materials'),

    path('daily_report/', daily_report, name='daily_report'),

    path('orders/', LoanedOrderAllListView.as_view(), name='all_orders'),

    path('order_search/', order_search, name='order_search'),

    path('create_order/', create_order, name='create_order'),
    # Другие URL-маршруты
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)