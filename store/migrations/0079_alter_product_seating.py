# Generated by Django 4.2.1 on 2024-09-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0078_alter_product_seating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seating',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
