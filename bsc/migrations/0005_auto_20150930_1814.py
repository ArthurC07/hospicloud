# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0004_auto_20150929_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meta',
            name='tipo_meta',
            field=models.CharField(default=b'CT', max_length=3, choices=[(b'CT', 'Tiempo de Consulta'), (b'PCT', 'Tiempo en Preconsulta'), (b'PP', 'Porcentaje de Recetas'), (b'IP', 'Porcentaje de Incapacidades'), (b'CFP', 'Porcentaje de Aprobaci\xf3n del Cliente'), (b'CR', 'Consulta Remitida a Especialista'), (b'CO', 'Coaching'), (b'PU', 'Puntualidad'), (b'QJ', 'Manejo de Quejas'), (b'VE', 'Ventas del Mes'), (b'PR', 'Manejo de Presupuesto'), (b'TU', 'Manejo de Turnos'), (b'TE', 'Horas Ense\xf1adas'), (b'EV', 'Evaluaci\xf3n de Alumnos'), (b'CA', 'Capacitaciones')]),
        ),
    ]
