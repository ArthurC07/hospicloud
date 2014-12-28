# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiario',
            name='inscripcion',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 19000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cancelacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 24000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contrato',
            name='ultimo_pago',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 17000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 23000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meta',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 23000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 20000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
