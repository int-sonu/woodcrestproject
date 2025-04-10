# Generated by Django 4.2.1 on 2024-08-26 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_remove_sellerprofile_gst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerprofile',
            name='business_pan_card',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='cheque_passbook_photo',
            field=models.ImageField(upload_to='uploads/cheques_passbooks/'),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sellerprofile',
            name='sign',
            field=models.ImageField(upload_to='uploads/signatures/'),
        ),
    ]
