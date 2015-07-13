# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_compra_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcotizado',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
