# Generated by Django 4.2.1 on 2024-08-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_alter_seller_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('blocked', 'Blocked')], default='active', max_length=10),
        ),
    ]
