# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_gasto_periodo_de_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='fecha_de_pago',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='fecha_maxima_de_pago',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='periodo_de_pago',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
