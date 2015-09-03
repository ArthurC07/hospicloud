# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0013_auto_20150826_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='comprobante_entregado',
            field=models.BooleanField(default=False),
        ),
    ]
