# Generated by Django 4.2.1 on 2024-08-17 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_delete_feedback_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('blocked', 'Blocked')], default='active', max_length=10),
        ),
    ]
