# Generated by Django 4.2.1 on 2024-10-24 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0128_orders_delivered_at_orders_out_for_delivery_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='delivered_at',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='estimated_delivery',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='out_for_delivery_at',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='packed_at',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='shipped_at',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='tracking_info',
        ),
    ]