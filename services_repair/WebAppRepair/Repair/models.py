from django.db import models

# Create your models here.

class Product_Type(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

class Type_of_pockets(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')

class Size(models.Model):
    russian_size = models.CharField(max_length=3, verbose_name='Российский размер')
    international_size = models.CharField(max_length=3, verbose_name='Международный размер')

class Product_Type(models.Model):
    name = models.CharField(max_length=60, verbose_name='Вид изделия')

class Product(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название изделия')
    description = models.TextField(verbose_name='Описание изделия')
    decorative_elements = models.TextField(verbose_name='Декоративные элементы')
    features = models.TextField(verbose_name='Особенности модели')
    main_fabric = models.CharField(max_length=120, verbose_name='Основная ткань')
    image = models.ImageField(blank=True, verbose_name='Изображение')
