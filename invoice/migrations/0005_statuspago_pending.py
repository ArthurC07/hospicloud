# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_conceptodeduccion_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuspago',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]
