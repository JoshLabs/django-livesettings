# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-05-16 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livesettings', '0002_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='longsetting',
            name='version',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='setting',
            name='version',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
