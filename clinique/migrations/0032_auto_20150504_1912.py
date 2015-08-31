# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0031_tipoconsulta_facturable'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='consulta',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='consulta',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='consulta',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='consulta',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
    ]
