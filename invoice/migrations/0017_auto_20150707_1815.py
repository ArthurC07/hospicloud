# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0016_auto_20150704_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cierreturno',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
    ]
