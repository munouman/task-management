# Generated by Django 5.1.7 on 2025-03-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_task_assigned_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
