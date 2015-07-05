# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0015_venta_monto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
