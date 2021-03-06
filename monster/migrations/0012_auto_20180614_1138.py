# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-14 11:38
from __future__ import unicode_literals

from django.db import migrations

def number_monsters(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Monster = apps.get_model("monster", "Monster")
    for i, m in enumerate(Monster.objects.all()):
        m.number = i+1
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('monster', '0011_auto_20180614_1138'),
    ]

    operations = [
        migrations.RunPython(number_monsters),
    ]
