# Generated by Django 4.2.1 on 2024-08-25 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_remove_passwordcreation_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BankDetails',
        ),
        migrations.DeleteModel(
            name='BusinessDetails',
        ),
        migrations.DeleteModel(
            name='PasswordCreation',
        ),
        migrations.DeleteModel(
            name='SellerRegistration',
        ),
    ]