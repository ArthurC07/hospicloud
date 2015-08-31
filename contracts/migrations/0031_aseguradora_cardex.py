# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0012_persona_rtn'),
        ('contracts', '0030_auto_20150528_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='cardex',
            field=models.ForeignKey(related_name='cardex', blank=True, to='persona.Persona', null=True),
        ),
    ]
