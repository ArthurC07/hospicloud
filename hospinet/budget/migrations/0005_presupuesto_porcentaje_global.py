# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_gasto_comprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='porcentaje_global',
            field=models.DecimalField(default=decimal.Decimal, max_digits=3, decimal_places=2),
        ),
    ]
