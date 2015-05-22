# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_recibo_correlativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnocaja',
            name='apertura',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
        ),
    ]
