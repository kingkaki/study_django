# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-22 16:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoureseComments',
            new_name='CourseComments',
        ),
    ]
