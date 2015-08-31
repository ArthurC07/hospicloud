# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150507_1637'),
        ('persona', '0012_persona_rtn'),
        ('contracts', '0028_auto_20150526_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='aseguradora',
            name='representante',
            field=models.ForeignKey(related_name='aseguradoras', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='rtn',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='item',
            field=models.ForeignKey(blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='nombre',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
