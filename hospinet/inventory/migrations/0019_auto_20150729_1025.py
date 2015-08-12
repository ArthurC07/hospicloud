# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_proveedor_rtn'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='contacto',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='direccion',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
