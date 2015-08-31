# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_auto_20150814_1108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuenta',
            options={'ordering': ('nombre',)},
        ),
        migrations.AddField(
            model_name='gasto',
            name='numero_pagos',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='gasto',
            name='proximo_pago',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
