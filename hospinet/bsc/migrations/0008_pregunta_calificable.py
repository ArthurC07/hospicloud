# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0007_remove_pregunta_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='calificable',
            field=models.BooleanField(default=True),
        ),
    ]
