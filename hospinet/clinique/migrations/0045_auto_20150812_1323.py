# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0044_prescripcion_dosis'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='revisada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='especialista',
            field=models.BooleanField(default=False),
        ),
    ]
