# Generated by Django 4.2.1 on 2024-08-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_delete_bankdetails_delete_businessdetails_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerRegistration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('otp_email', models.CharField(blank=True, max_length=6, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('sell_category', models.CharField(choices=[('all_categories', 'All Categories')], default='all_categories', max_length=50)),
                ('gstin', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]