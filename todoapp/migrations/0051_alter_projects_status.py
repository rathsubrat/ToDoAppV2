# Generated by Django 5.0.6 on 2024-07-29 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0050_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todoapp.card'),
        ),
    ]