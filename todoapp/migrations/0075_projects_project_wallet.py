# Generated by Django 5.0.7 on 2024-08-07 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0074_task_enddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='project_wallet',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
