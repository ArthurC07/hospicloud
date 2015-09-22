# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20150922_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuente',
            name='caja',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gasto',
            name='fecha_de_recepcion_de_factura',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='numero_de_comprobante_de_pago',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
