# Generated by Django 5.0.6 on 2024-07-29 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0055_alter_projects_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='status',
        ),
    ]
