# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0002_consultorio_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='motivo_de_consulta',
            field=models.TextField(default=None, null=True),
            preserve_default=True,
        ),
    ]
