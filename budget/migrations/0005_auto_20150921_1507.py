# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_auto_20150920_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gasto',
            name='aseguradora',
        ),
        migrations.AddField(
            model_name='fuente',
            name='monto',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2),
        ),
        migrations.AddField(
            model_name='gasto',
            name='factura',
            field=models.FileField(null=True, upload_to=b'budget/gasto/%Y/%m/%d', blank=True),
        ),
    ]
