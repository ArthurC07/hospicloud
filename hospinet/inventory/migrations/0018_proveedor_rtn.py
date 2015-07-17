# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_itemcotizado_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='rtn',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
