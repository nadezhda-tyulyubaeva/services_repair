# Generated by Django 4.2.7 on 2023-11-20 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Repair', '0007_order_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата изменения статуса заказа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Repair.employee', verbose_name='Сотрудник')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Repair.order', verbose_name='Заказ')),
                ('order_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Repair.status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Статусы заказов',
                'ordering': ['date'],
            },
        ),
    ]
