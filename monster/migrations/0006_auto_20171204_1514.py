# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monster', '0005_auto_20171204_0101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monster',
            old_name='image',
            new_name='record_image',
        ),
        migrations.AddField(
            model_name='monster',
            name='monster_image',
            field=models.ImageField(null=True, upload_to='uploads/monsters/'),
        ),
    ]
