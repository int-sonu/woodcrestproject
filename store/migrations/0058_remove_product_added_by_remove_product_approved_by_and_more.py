# Generated by Django 4.2.1 on 2024-08-30 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0057_remove_product_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='product',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='product',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_approved',
        ),
    ]
