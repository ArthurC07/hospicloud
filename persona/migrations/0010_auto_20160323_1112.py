# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0009_auto_20160322_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fisico',
            name='altura',
        ),
        migrations.RemoveField(
            model_name='fisico',
            name='bmi',
        ),
        migrations.RemoveField(
            model_name='fisico',
            name='bmr',
        ),
        migrations.RemoveField(
            model_name='fisico',
            name='medida_de_peso',
        ),
    ]
