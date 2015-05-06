# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0033_diagnosticoclinico_consulta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosticoclinico',
            name='diagnostico',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
