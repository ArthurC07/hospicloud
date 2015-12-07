# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_cotizacion_credito'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='terminada',
            field=models.BooleanField(default=False),
        ),
    ]
