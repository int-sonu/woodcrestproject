# Generated by Django 4.2.1 on 2024-08-28 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_seller_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='role',
        ),
    ]