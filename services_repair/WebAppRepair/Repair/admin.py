from django.contrib import admin
#from django_object_actions import DjangoObjectActions

# Register your models here.

from .models import *

admin.site.register([Client,
                     Employee,
                     Material,
                     Materials_accounting_journal,
                     Product_Type,
                     Type_of_pockets,
                     Size,
                     Color,
                     Type_of_fastener,
                     Measure,
                     Status,
                     Unit_of_measurement,
                     Service,
                     Stock,
                     Product,
                     CustomUser,
                     Map_of_measurements])

class Price_list_services_pozitionInline(admin.TabularInline):
    model = Price_list_services_pozition


class Price_list_servicesAdmin(admin.ModelAdmin):
    inlines = [Price_list_services_pozitionInline]
    # search_fields = ("title__startswith",)


admin.site.register(Price_list_services, Price_list_servicesAdmin)

class Price_list_material_pozitionInline(admin.TabularInline):
    model = Price_list_material_pozition


class Price_list_materialAdmin(admin.ModelAdmin):
    inlines = [Price_list_material_pozitionInline]
    # search_fields = ("title__startswith",)


admin.site.register(Price_list_material, Price_list_materialAdmin)

class Materials_orderInline(admin.TabularInline):
    model = Materials_order

class Map_of_measurementsInline(admin.TabularInline):
    model = Map_of_measurements

class Order_pozitionInline(admin.TabularInline):
    model = Order_pozition

class Order_statusInline(admin.TabularInline):
    model = Order_status




class OrderAdmin(admin.ModelAdmin):
    inlines = ([Materials_orderInline, Map_of_measurementsInline, Order_pozitionInline, Order_statusInline])
    fieldsets = [
        (None, {'fields': [('number', 'date'), 'client', 'product', 'NDS']}),
        ('ПРИМЕРКА', {'fields': [('date_of_the_first_fitting', 'date_of_the_second_fitting'),]}),
        ('ИЗГОТОВЛЕНИЕ', {'fields': [('planned_production_date', 'actual_production_date'), ]}),
        #('Сумма заказа', {'fields': ['total_atelier_materials_cost', 'total_client_materials_cost', ]}),
    ]
    list_filter = ('date', 'client',)

    change_form_template = "admin/change_form.html"  # Here

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['custom_button'] = True  # Here

        return super().changeform_view(request, object_id, form_url, extra_context)

    def response_add(self, request, obj, post_url_continue=None):  # Here

        if "_custom_button" in request.POST:
            # Do something
            return super().response_add(request, obj, post_url_continue)
        else:
            # Do something
            return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):  # Here

        if "_custom_button" in request.POST:
            # Do something
            return super().response_change(request, obj)
        else:
            # Do something
            return super().response_change(request, obj)
    # search_fields = ("title__startswith",)


admin.site.register(Order, OrderAdmin)

admin.site.site_title = 'Главная страница'
admin.site.index_title = 'Главная страница'
admin.site.site_header = 'Администрирование сайта ателье по ремонту одежды'
