# Generated by Django 4.2.1 on 2024-08-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0047_remove_seller_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]