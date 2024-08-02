# Generated by Django 4.2.6 on 2024-06-12 01:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('done_date', models.DateTimeField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='media/')),
                ('priority', models.IntegerField(default=1)),
                ('assigned_to', models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
