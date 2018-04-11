# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('livesettings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='longsetting',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Created at'),
        ),
        migrations.AddField(
            model_name='longsetting',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Updated At', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='longsetting',
            name='updated_by',
            field=models.CharField(help_text=b'Tracks who updated the record', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='longsetting',
            name='updated_through',
            field=models.CharField(help_text=b'Tracks channel through which record was updated', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='longsetting',
            name='updating_process',
            field=models.CharField(help_text=b'Tracks the process/method updating the record', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='longsetting',
            name='updating_process_meta',
            field=models.TextField(help_text=b'Contains meta information regarding process updating record like File Name etc.', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Created at'),
        ),
        migrations.AddField(
            model_name='setting',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Updated At', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='setting',
            name='updated_by',
            field=models.CharField(help_text=b'Tracks who updated the record', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='updated_through',
            field=models.CharField(help_text=b'Tracks channel through which record was updated', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='updating_process',
            field=models.CharField(help_text=b'Tracks the process/method updating the record', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='setting',
            name='updating_process_meta',
            field=models.TextField(help_text=b'Contains meta information regarding process updating record like File Name etc.', editable=False, blank=True),
        ),
    ]
