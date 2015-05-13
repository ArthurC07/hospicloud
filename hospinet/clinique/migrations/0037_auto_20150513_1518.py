# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0036_prescripcion_medicamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescripcion',
            name='nota',
            field=models.TextField(verbose_name='Otros MEdicamentos', blank=True),
            preserve_default=True,
        ),
    ]
