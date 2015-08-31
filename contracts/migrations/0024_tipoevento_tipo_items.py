# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_vencimiento'),
        ('contracts', '0023_auto_20150504_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoevento',
            name='tipo_items',
            field=models.ForeignKey(related_name='tipo_eventos', blank=True, to='inventory.ItemType', null=True),
            preserve_default=True,
        ),
    ]
