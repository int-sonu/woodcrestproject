# Generated by Django 4.2.1 on 2024-09-04 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0089_dimension'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimension',
            name='backrest_height',
        ),
        migrations.RemoveField(
            model_name='dimension',
            name='mattress_size',
        ),
        migrations.RemoveField(
            model_name='dimension',
            name='seat_depth',
        ),
        migrations.RemoveField(
            model_name='dimension',
            name='seat_height',
        ),
    ]
