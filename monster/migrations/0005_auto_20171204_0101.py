# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 01:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monster', '0004_monster_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/monsters/'),
        ),
    ]
