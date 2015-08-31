# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_historial_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
