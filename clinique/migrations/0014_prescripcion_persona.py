# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
        ('clinique', '0013_auto_20150424_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='persona',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
    ]
