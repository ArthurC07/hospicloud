# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-10 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0011_auto_20160404_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='cargo',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
