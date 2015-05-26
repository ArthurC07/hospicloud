# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0027_auto_20150524_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficio',
            name='aplicar_a_suspendidos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contrato',
            name='suspendido',
            field=models.BooleanField(default=False),
        ),
    ]
