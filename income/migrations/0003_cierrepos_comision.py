# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_auto_20160119_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='cierrepos',
            name='comision',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
        ),
    ]