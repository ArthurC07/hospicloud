# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0041_consulta_encuestada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescripcion',
            name='consulta',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='nota',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='persona',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='orden',
            field=models.ForeignKey(blank=True, to='clinique.OrdenMedica', null=True),
        ),
    ]
