# Generated by Django 5.0.6 on 2024-07-23 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0043_alter_task_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Project',
        ),
    ]
