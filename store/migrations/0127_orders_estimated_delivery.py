# Generated by Django 4.2.1 on 2024-10-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0126_orders_tracking_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='estimated_delivery',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
