# Generated by Django 4.2.1 on 2024-09-03 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0085_remove_seat_seat_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='seat_color',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='seat_material',
        ),
        migrations.AddField(
            model_name='seat',
            name='seat_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]