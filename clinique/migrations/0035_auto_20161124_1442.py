# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0034_auto_20161123_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='satisfaccion',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='seguimiento',
            field=models.BooleanField(default=False),
        ),
    ]