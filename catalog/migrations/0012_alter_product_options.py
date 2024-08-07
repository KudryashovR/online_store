# Generated by Django 5.0.7 on 2024-07-17 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_cancel_publication', 'Can cancel publication of product'), ('can_change_description', 'Can change description of product'), ('can_change_category', 'Can change category of product')], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
