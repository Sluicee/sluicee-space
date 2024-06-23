# Generated by Django 5.0.6 on 2024-06-23 09:08

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, editable=False, populate_from='title', unique=True),
        ),
    ]
