# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0004_consulta_hea'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='atendida',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
