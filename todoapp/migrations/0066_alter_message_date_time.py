# Generated by Django 5.0.6 on 2024-08-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0065_alter_message_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]