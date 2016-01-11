# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_tipoventa_predeterminada'),
        ('invoice', '0005_statuspago_pending'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comprobantededuccion',
            name='persona',
        ),
        migrations.AddField(
            model_name='comprobantededuccion',
            name='proveedor',
            field=models.ForeignKey(to='inventory.Proveedor', null=True),
        ),
    ]
