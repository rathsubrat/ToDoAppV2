# Generated by Django 5.0.6 on 2024-07-29 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0056_remove_projects_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='status',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='todoapp.card'),
        ),
    ]