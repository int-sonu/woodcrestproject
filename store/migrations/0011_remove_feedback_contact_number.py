# Generated by Django 4.2.1 on 2024-08-13 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='contact_number',
        ),
    ]
