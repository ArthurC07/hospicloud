# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0039_consulta_remitida'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenmedica',
            name='evolucion',
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='medicamento',
        ),
    ]
