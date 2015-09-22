# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_auto_20150922_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='numero_de_factura',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
