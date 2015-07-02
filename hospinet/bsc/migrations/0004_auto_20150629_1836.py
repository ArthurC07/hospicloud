# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import emergency.models


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0003_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='tipo_extra',
            field=models.CharField(default=emergency.models.Emergencia, max_length=3, choices=[(b'ER', 'Emergencias Atendidas')]),
        ),
        migrations.AlterField(
            model_name='meta',
            name='tipo_meta',
            field=models.CharField(default=b'CT', max_length=3, choices=[(b'CT', 'Tiempo de Consulta'), (b'PCT', 'Tiempo en Preconsulta'), (b'PP', 'Porcentaje de Recetas'), (b'IP', 'Porcentaje de Incapacidades'), (b'CFP', 'Porcentaje de Aprobaci\xf3n del Cliente'), (b'CR', 'Consulta Remitida a Especialista')]),
        ),
    ]
