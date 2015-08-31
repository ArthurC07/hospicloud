# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
        ('clinique', '0012_auto_20150424_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='consultorio',
            field=models.ForeignKey(related_name='cargos', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cargo',
            name='persona',
            field=models.ForeignKey(related_name='cargos', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='consultorio',
            field=models.ForeignKey(related_name='consultas', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='final',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='persona',
            field=models.ForeignKey(related_name='consultas', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='consultorio',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='persona',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='consultorio',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='persona',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='persona',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='consultorio',
            field=models.ForeignKey(related_name='notas_enfermeria', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='persona',
            field=models.ForeignKey(related_name='notas_enfermeria', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='consultorio',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='persona',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='consultorio',
            field=models.ForeignKey(related_name='seguimientos', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='persona',
            field=models.ForeignKey(related_name='seguimientos', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consulta',
            name='activa',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
