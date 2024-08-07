# Generated by Django 5.0.6 on 2024-07-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0062_task_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='taskName',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
