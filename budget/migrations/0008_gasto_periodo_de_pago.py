# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0007_gasto_fecha_de_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='periodo_de_pago',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
