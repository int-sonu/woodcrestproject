# Generated by Django 4.2.1 on 2024-09-04 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0095_delete_customcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CustomSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_subcategories', to='store.customcategory')),
            ],
        ),
    ]
