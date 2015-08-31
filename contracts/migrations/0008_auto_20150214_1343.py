# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0007_mastercontract_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficio',
            name='activo',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficio',
            name='observacion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beneficio',
            name='valor',
            field=models.DecimalField(default=0, verbose_name=b'precio', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
