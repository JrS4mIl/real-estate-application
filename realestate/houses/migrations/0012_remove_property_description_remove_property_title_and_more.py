# Generated by Django 5.1.6 on 2025-02-15 14:40

import django.db.models.deletion
import parler.fields
import parler.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0011_alter_category_name_alter_property_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='description',
        ),
        migrations.RemoveField(
            model_name='property',
            name='title',
        ),
        migrations.CreateModel(
            name='PropertyTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(max_length=400, verbose_name='description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='houses.property')),
            ],
            options={
                'verbose_name': 'property Translation',
                'db_table': 'houses_property_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]
