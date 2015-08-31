# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_remove_compra_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(blank=True, to='inventory.Proveedor', null=True),
        ),
    ]
