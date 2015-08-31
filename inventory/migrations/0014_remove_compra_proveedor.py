# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_cotizacion_itemcotizado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='proveedor',
        ),
    ]
