# Generated by Django 4.2.1 on 2024-09-06 09:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0100_customrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customrequest',
            name='description',
        ),
        migrations.AddField(
            model_name='customrequest',
            name='custom_requirements',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customrequest',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]
