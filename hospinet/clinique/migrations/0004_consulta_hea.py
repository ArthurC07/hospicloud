# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0003_consulta_motivo_de_consulta'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='HEA',
            field=models.TextField(default=None, null=True),
            preserve_default=True,
        ),
    ]
