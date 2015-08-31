# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_auto_20150615_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='impuesto',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2, blank=True),
        ),
    ]
