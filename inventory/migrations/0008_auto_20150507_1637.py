# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_itemtype_consulta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtemplate',
            name='item_type',
            field=models.ManyToManyField(related_name='items', to='inventory.ItemType', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itemtemplate',
            name='suppliers',
            field=models.ManyToManyField(related_name='plantillas', to='inventory.Proveedor', blank=True),
            preserve_default=True,
        ),
    ]
