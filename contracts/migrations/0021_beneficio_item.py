# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_vencimiento'),
        ('contracts', '0020_remove_plan_consulta_horario_extendido'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficio',
            name='item',
            field=models.ForeignKey(related_name='beneficios', blank=True, to='inventory.ItemTemplate', null=True),
            preserve_default=True,
        ),
    ]
