# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0011_pregunta_mostrar_sugerencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='terminada',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
