from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

TYPE_MATERIAL = (
    ('Клиента', 'Клиента'),
    ('Ателье', 'Ателье')
    )

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to="images", blank=True, verbose_name='Изображение')
    middle_name = models.CharField("Отчество", max_length=50, null=True, blank=True)
    number = models.CharField("Номер телефона", max_length=18)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Product_Type(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид изделия"
        verbose_name_plural = "Виды изделий"


class Type_of_pockets(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип карманов"
        verbose_name_plural = "Типы карманов"


class Size(models.Model):
    russian_size = models.CharField(max_length=3, verbose_name='Российский размер')
    international_size = models.CharField(max_length=3, verbose_name='Международный размер')

    def __str__(self):
        return f"{self.international_size} ({self.russian_size})"

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Color(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Type_of_fastener(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид застежки"
        verbose_name_plural = "Виды застежки"


class Measure(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мерка"
        verbose_name_plural = "Мерки"


class Product(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название изделия')
    description = models.TextField(verbose_name='Описание изделия')
    decorative_elements = models.TextField(verbose_name='Декоративные элементы')
    features = models.TextField(verbose_name='Особенности модели')
    main_fabric = models.CharField(max_length=120, verbose_name='Основная ткань')
    image = models.ImageField(upload_to="images", blank=True, verbose_name='Изображение')
    color = models.ForeignKey('Color', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Цвет")
    product_type = models.ForeignKey('Product_Type', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="Вид изделия")
    type_of_pockets = models.ForeignKey('Type_of_pockets', on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Тип карманов")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Размер")
    type_of_fastener = models.ForeignKey('Type_of_fastener', on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name="Вид застежки")

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"
    def __str__(self):
        return f"{self.name}"

class Employee(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Пользователь")
    date_of_acceptance = models.DateField(blank=True, null=True, verbose_name="Дата принятия")
    date_of_dismissal = models.DateField(blank=True, null=True, verbose_name="Дата увольнения")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Client(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Пользователь")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    discount = models.IntegerField(blank=True, null=True, verbose_name='Персональная скидка')

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Status(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class  Unit_of_measurement(models.Model):
     full_name = models.CharField(max_length=60, verbose_name='Полное наименование')
     short_name = models.CharField(max_length=60, verbose_name='Краткое наименование')
     def __str__(self):
        return self.full_name

     class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

class Service(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Material(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    description = models.TextField(verbose_name='Описание материала')
    image = models.ImageField(upload_to="images", blank=True, verbose_name='Изображение')
    type_material = models.CharField(max_length=120, null=True, verbose_name="Вид материала", choices=TYPE_MATERIAL)
    unit_of_measurement = models.ForeignKey('Unit_of_measurement', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Единица измерения")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

class Material_characteristics(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    value = models.TextField(verbose_name='Значение')
    material = models.ForeignKey('Material', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Материал")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Характеристика материала"
        verbose_name_plural = "Характеристики материала"

class Product_composition(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Изделие")
    material = models.ForeignKey('Material', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Материал")
    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Состав изделия"
        verbose_name_plural = "Составы изделий"

class Stock(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Процент скидки')
    start = models.DateField('Дата начала действия')
    end = models.DateField('Дата окончания действия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

class Price_list_services(models.Model):
    number = models.IntegerField(verbose_name="Номер прайс-листа")
    date = models.DateField(blank=True, null=True, verbose_name="Дата утверждения прайс-листа", auto_now_add=True)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сотрудник")
    def __str__ (self):
        return 'Прайс-лист № %s от %s' % (self.number, self.date)

    class Meta:
        ordering = ['number']
        verbose_name = "Прайс-лист на услуги"
        verbose_name_plural = "Прайс-листы на услуги"

class Price_list_material(models.Model):
    number = models.IntegerField(verbose_name="Номер прайс-листа")
    date = models.DateField(blank=True, null=True, verbose_name="Дата утверждения прайс-листа", auto_now_add=True)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сотрудник")
    def __str__ (self):
        return 'Прайс-лист № %s от %s' % (self.number, self.date)

    class Meta:
        ordering = ['number']
        verbose_name = "Прайс-лист на материалы"
        verbose_name_plural = "Прайс-листы на материалы"

class Price_list_material_pozition(models.Model):
    cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True,verbose_name="Цена материала в прайс-листе, руб.")
    material = models.ForeignKey('Material', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Материал")
    price_list = models.ForeignKey('Price_list_material', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Прайс-лист")
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сотрудник")

    def __str__(self):
        return 'Материал %s: %s (стоимость: %s руб.)' % (self.material.type_material, self.material.name, self.cost)


    class Meta:
        ordering = ['cost']
        verbose_name = "Позиция прайс-листа на материалы"
        verbose_name_plural = "Позиции прайс-листа на материалы"

class Price_list_services_pozition(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Услуга")
    cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True,verbose_name="Цена услуги в прайс-листе, руб.")
    price_list = models.ForeignKey('Price_list_services', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Прайс-лист")

    def __str__(self):
        return 'Услуга: %s (стоимость: %s руб.)' % (self.service.name, self.cost)


    class Meta:
        ordering = ['cost']
        verbose_name = "Позиция прайс-листа на услуги"
        verbose_name_plural = "Позиции прайс-листа на услуги"
class Materials_accounting_journal(models.Model):
    start = models.DateField(blank=True, null=True, verbose_name="Дата начала")
    end = models.DateField(blank=True, null=True, verbose_name="Дата окончания")
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сотрудник")
    def __str__ (self):
        return 'Журнал учета материалов с %s по %s' % (self.start, self.end)

    class Meta:
        verbose_name = "Журнал учета материалов"
        verbose_name_plural = "Журналы учета материалов"

class Materials_accounting_journal_pozition(models.Model):
    date = models.DateField(blank=True, null=True, verbose_name="Дата")
    remains_start = models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True,verbose_name="Остаток на начало дня")
    remains_end = models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True,verbose_name="Остаток на конец дня")
    material = models.ForeignKey('Material', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Материал")
    unit_of_measurement = models.ForeignKey('Unit_of_measurement', on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Единица измерения")
    journal = models.ForeignKey('Materials_accounting_journal', on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Журнал учета материалов")
    def __str__ (self):
        return 'Дата: %s, материал: %s, остаток: %s' % (self.date, self.material, self.remains_end)

class Order(models.Model):
    number = models.IntegerField('Номер')
    date = models.DateField(blank=True, null = True, verbose_name='Дата')
    date_of_the_first_fitting = models.DateField(blank=True, null = True, verbose_name='Дата первой примерки')
    date_of_the_second_fitting = models.DateField(blank=True, null=True, verbose_name='Дата второй примерки')
    planned_production_date = models.DateField(blank=True, null=True, verbose_name='Плановая дата изготовления')
    actual_production_date = models.DateField(blank=True, null=True, verbose_name='Фактическая дата изготовления')
    NDS = models.IntegerField(verbose_name="Ставка НДС")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Клиент")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Изделие")


    def __str__(self):
        return f"Заказ №{self.number} от {self.date} (клиент: {self.client})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Materials_order(models.Model):

    pozition = models.ForeignKey(Price_list_material_pozition, on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Позиция прайс-листа")
    unit_of_measurement = models.ForeignKey('Unit_of_measurement', on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Единица измерения")
    count = models.IntegerField('Количество')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Заказ")

    @property
    def total_cost(self):
        if self.pozition and self.pozition.cost:
            return self.count * self.pozition.cost
        else:
            return 0

    def __str__(self):
        return f"Заказ {self.order.id}, Позиция {self.pozition.id}, Количество: {self.count}, Итог: {self.total_cost} руб."

    class Meta:
        verbose_name = "Материал к заказу"
        verbose_name_plural = "Материалы к заказу"

class Order_status(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Заказ")
    order_status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Статус")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Дата изменения статуса заказа")
    comment = models.TextField(blank=True, null = True, verbose_name = "Комментарий")
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Сотрудник")


    def __str__(self):
            return '%s %s' % (self.order, self.order_status)

    class Meta:
            ordering = ['date']
            verbose_name="Заказ"
            verbose_name_plural="Статусы заказов"

class Order_pozition(models.Model):
    service = models.ForeignKey('Price_list_services_pozition', on_delete=models.CASCADE, blank=True,null=True, verbose_name="Наименование услуги")
    unit_of_measurement = models.ForeignKey('Unit_of_measurement', on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name="Единица измерения")
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Заказ")
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Акция")

    @property
    def total_order_cost_with_discount(self):
        if self.service and self.service.cost:
            discount = self.stock.discount

        if self.stock and discount is not None:
            discount_amount = (self.service.cost * discount) / 100
            total_cost_with_discount = self.service.cost - discount_amount
            return total_cost_with_discount
        else:
            return self.service.cost

    def __str__(self):
        return 'Услуга %s: %s (стоимость c учетом скидки: %s руб.)' % (self.service.service.name, self.service.cost, self.total_order_cost_with_discount)


    class Meta:
        verbose_name = "Наименование работ"
        verbose_name_plural = "Наименование работ"

class Map_of_measurements(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Заказ")
    measure = models.ForeignKey('Measure', on_delete=models.SET_NULL, blank=True,null=True, verbose_name='Мерка')
    value = models.DecimalField(max_digits=7, decimal_places=2, blank=True,null=True,verbose_name="Значение мерки, см")
    def __str__ (self):
        return f"Карта мерок ({self.order})"

    class Meta:
        verbose_name = "Карта мерок"
        verbose_name_plural = "Карта мерок"
