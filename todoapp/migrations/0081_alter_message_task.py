# Generated by Django 5.0.7 on 2024-08-09 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0080_projects_eta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='todoapp.task'),
        ),
    ]