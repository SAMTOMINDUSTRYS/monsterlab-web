# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-14 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monster', '0012_auto_20180614_1138'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monster',
            unique_together=set([('event', 'number')]),
        ),
    ]
