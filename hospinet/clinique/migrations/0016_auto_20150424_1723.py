# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0015_auto_20150424_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='diagnosticoclinico',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='incapacidad',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='notaenfermeria',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='seguimiento',
            name='paciente',
        ),
    ]
