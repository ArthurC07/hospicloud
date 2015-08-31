# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_auto_20141227_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiario',
            name='inscripcion',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 372000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cancelacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 384000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contrato',
            name='ultimo_pago',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 368000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 380000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meta',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 382000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 375000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
