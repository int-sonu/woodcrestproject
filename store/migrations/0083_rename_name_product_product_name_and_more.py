# Generated by Django 4.2.1 on 2024-09-03 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0082_rename_product_name_product_name_product_material_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='material',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seating',
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.subcategory'),
        ),
        migrations.DeleteModel(
            name='SeatingOption',
        ),
    ]