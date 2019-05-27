# Generated by Django 2.1 on 2019-05-27 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20190527_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='dashboard.Category', null=True),
            preserve_default=False,
        ),
    ]
