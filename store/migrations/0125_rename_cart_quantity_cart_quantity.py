# Generated by Django 4.2.1 on 2024-10-24 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0124_rename_cart_quantity_orders_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart_quantity',
            new_name='quantity',
        ),
    ]