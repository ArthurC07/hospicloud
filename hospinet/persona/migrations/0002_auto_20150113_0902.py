# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='fotografia',
            field=models.ImageField(help_text=b'El archivo debe estar en formato jpg o png y no pesar mas de 120kb', null=True, upload_to=b'persona/foto//%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='tipo_identificacion',
            field=models.CharField(blank=True, max_length=1, choices=[(b'R', 'Carnet de Residencia'), (b'L', 'Licencia'), (b'P', 'Pasaporte'), (b'T', 'Tarjeta de Identidad'), (b'N', 'Ninguno')]),
            preserve_default=True,
        ),
    ]
