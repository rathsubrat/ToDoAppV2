# Generated by Django 5.0.6 on 2024-07-22 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0037_projects_manager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='done_date',
            new_name='dead_line',
        ),
        migrations.RemoveField(
            model_name='task',
            name='start_date',
        ),
    ]
