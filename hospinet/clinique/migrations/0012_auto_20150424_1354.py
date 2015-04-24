# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0011_auto_20150422_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='facturado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='activa',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='facturada',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='consulta',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cargo',
            name='tipo',
            field=models.ForeignKey(related_name='cargos', to='inventory.ItemType'),
            preserve_default=True,
        ),
    ]
