# Generated by Django 5.0.6 on 2024-07-31 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0061_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='enddate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
