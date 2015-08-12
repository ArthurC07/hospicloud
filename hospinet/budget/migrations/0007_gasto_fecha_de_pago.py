# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20150731_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='fecha_de_pago',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
