# Generated by Django 5.0.7 on 2024-08-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0068_task_task_progress_alter_task_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='enddate',
        ),
        migrations.AddField(
            model_name='task',
            name='achieved_points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='approvals',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Completed'),
        ),
        migrations.AddField(
            model_name='task',
            name='is_flaged',
            field=models.BooleanField(default=False, verbose_name='Flaged'),
        ),
    ]
