# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_proveedor_rtn'),
        ('budget', '0002_presupuesto_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='cheque',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='gasto',
            name='proveedor',
            field=models.ForeignKey(blank=True, to='inventory.Proveedor', null=True),
        ),
    ]
