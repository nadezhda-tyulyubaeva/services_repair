# Generated by Django 4.2.7 on 2023-11-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Repair', '0005_alter_product_options_alter_product_type_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials_order',
            name='unit_of_measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Repair.unit_of_measurement', verbose_name='Единица измерения'),
        ),
    ]
