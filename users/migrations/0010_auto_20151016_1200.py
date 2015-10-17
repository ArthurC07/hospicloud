# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20151005_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='cai_comprobante',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='cai_recibo',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
