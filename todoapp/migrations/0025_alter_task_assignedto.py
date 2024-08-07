# Generated by Django 4.2.6 on 2024-07-18 05:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todoapp', '0024_task_tech_stack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignedTo',
            field=models.ManyToManyField(blank=True, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
