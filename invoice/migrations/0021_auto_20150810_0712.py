# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0020_cuentaporcobrar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(default=Decimal('0'), max_digits=11, decimal_places=2),
        ),
    ]
