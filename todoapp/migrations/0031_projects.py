# Generated by Django 5.0.6 on 2024-07-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0030_project_proj_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('deadline', models.DateField()),
                ('team', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('techStack', models.JSONField()),
            ],
        ),
    ]