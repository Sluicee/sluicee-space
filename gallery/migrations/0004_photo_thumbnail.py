# Generated by Django 5.0.6 on 2024-07-17 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_remove_photo_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='photos/thumbnails/'),
        ),
    ]