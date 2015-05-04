# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_vencimiento'),
        ('contracts', '0022_auto_20150504_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficio',
            name='item',
        ),
        migrations.AddField(
            model_name='beneficio',
            name='tipo_items',
            field=models.ForeignKey(related_name='beneficios', blank=True, to='inventory.ItemType', null=True),
            preserve_default=True,
        ),
    ]
