# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0010_presupuesto_inversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='factura',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
