# Generated by Django 4.2.7 on 2024-01-10 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Repair', '0014_rename_emloyee_order_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Квитанция'),
        ),
    ]
