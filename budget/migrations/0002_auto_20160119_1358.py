# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuestomes',
            name='completar_anio',
            field=models.BooleanField(default=False, verbose_name='Completar A\xf1o'),
        ),
        migrations.AlterField(
            model_name='presupuestomes',
            name='procesado',
            field=models.BooleanField(default=False),
        ),
    ]
