# Generated by Django 5.1.6 on 2025-02-18 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0012_remove_property_description_remove_property_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
    ]
