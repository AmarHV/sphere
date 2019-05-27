# Generated by Django 2.1 on 2019-05-27 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_project_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryAttributeWeighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weighting', models.FloatField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_attribute_weightings', to='dashboard.Attribute')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_attribute_weightings', to='dashboard.Category')),
            ],
        ),
    ]
