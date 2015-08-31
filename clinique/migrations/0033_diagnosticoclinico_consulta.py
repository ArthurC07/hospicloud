# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0032_auto_20150504_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='consulta',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
    ]
