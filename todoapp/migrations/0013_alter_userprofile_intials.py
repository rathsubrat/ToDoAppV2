# Generated by Django 4.2.6 on 2024-07-01 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0012_alter_userprofile_intials_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='intials',
            field=models.CharField(blank=True, default='<django.db.models.query_utils.DeferredAttribute object at 0x00000217C22A5A50>', max_length=50, null=True),
        ),
    ]
