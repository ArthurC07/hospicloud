# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0010_auto_20150218_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='activo',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='dependiente',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrato',
            name='certificado',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrato',
            name='poliza',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
