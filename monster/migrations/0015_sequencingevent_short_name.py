# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-22 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monster', '0014_auto_20180614_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequencingevent',
            name='short_name',
            field=models.CharField(db_index=True, default='SAM', max_length=8),
            preserve_default=False,
        ),
    ]
