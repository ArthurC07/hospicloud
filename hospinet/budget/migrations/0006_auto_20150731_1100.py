# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_presupuesto_porcentaje_global'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='ejecutado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gasto',
            name='fecha_maxima_de_pago',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
