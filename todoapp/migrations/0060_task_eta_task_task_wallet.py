# Generated by Django 5.0.6 on 2024-07-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0059_task_startdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='ETA',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_wallet',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
