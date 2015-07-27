# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0036_auto_20150606_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastercontract',
            name='gastos_medicos',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='vida',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
    ]
