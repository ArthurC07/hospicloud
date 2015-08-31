# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_pago_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='discount',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='tax',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
        ),
    ]
