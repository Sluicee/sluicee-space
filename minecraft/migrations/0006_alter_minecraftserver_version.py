# Generated by Django 5.0.6 on 2025-07-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minecraft', '0005_alter_minecraftserver_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minecraftserver',
            name='version',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Версия игры'),
        ),
    ]
