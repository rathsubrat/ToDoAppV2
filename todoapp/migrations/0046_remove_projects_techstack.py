# Generated by Django 5.0.6 on 2024-07-24 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0045_userprofile_assigned_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='techStack',
        ),
    ]
