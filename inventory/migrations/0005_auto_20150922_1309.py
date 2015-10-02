# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150921_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='constancia_de_pagos_a_cuenta',
            field=models.FileField(null=True, upload_to=b'inventory/provider/%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nombre Completo de la Empresa'),
        ),
    ]
