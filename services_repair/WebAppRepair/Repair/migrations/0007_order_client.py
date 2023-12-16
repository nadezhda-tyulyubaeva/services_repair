# Generated by Django 4.2.7 on 2023-11-20 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Repair', '0006_materials_order_unit_of_measurement'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Repair.client', verbose_name='Клиент'),
        ),
    ]