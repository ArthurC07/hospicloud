# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0005_cita_atendida'),
    ]

    operations = [
        migrations.AddField(
            model_name='incapacidad',
            name='dias',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
