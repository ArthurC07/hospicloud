# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-03 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20151130_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipopago',
            name='orden',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tipopago',
            name='reportable',
            field=models.BooleanField(default=True),
        ),
    ]
