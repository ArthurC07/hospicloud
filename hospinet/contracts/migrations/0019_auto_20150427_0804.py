# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_vencimiento'),
        ('contracts', '0018_auto_20150422_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='consulta',
            field=models.ForeignKey(related_name='plan', blank=True, to='inventory.ItemTemplate', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plan',
            name='consulta_horario_extendido',
            field=models.ForeignKey(related_name='plan_extendido', blank=True, to='inventory.ItemTemplate', null=True),
            preserve_default=True,
        ),
    ]
