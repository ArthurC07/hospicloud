# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_historial_fecha'),
        ('contracts', '0032_auto_20150529_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='item',
            field=models.ForeignKey(related_name='planes_precio', blank=True, to='inventory.ItemTemplate', null=True),
        ),
    ]
