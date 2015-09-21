# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20150921_1507'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gasto',
            old_name='comprobante',
            new_name='comprobante_de_pago',
        ),
        migrations.RenameField(
            model_name='gasto',
            old_name='periodo_de_pago',
            new_name='fecha_en_factura',
        ),
        migrations.RenameField(
            model_name='gasto',
            old_name='cheque',
            new_name='numero_de_comprobante_de_pago',
        ),
        migrations.RemoveField(
            model_name='gasto',
            name='proximo_pago',
        ),
    ]
