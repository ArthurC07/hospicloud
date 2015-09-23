# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0010_auto_20150922_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='numero_de_comprobante_de_pago',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
