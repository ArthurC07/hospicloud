# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('S', 'Soltero/a'), ('D', 'Divorciado/a'), ('C', 'Casado/a'), ('', 'Union Libre')], max_length=1),
        ),
    ]
