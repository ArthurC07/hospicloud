# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import persona.fields


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_venta_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipopago',
            name='color',
            field=persona.fields.ColorField(default=b'', max_length=10),
        ),
    ]
