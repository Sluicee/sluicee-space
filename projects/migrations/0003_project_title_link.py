# Generated by Django 5.0.6 on 2025-01-26 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='title_link',
            field=models.TextField(blank=True),
        ),
    ]
