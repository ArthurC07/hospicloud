# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0010_voto_sugerencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='mostrar_sugerencia',
            field=models.BooleanField(default=False),
        ),
    ]
