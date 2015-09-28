# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_comprobantededuccion_conceptodeduccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='conceptodeduccion',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]
