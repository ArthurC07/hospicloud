# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150110_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='plantilla',
            field=models.ForeignKey(related_name='items', verbose_name=b'Item', to='inventory.ItemTemplate'),
            preserve_default=True,
        ),
    ]
