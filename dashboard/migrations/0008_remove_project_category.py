# Generated by Django 2.1 on 2019-05-27 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_categoryattributeweighting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
    ]
