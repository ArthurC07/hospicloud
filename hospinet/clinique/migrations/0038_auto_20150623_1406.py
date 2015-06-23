# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_historial_fecha'),
        ('clinique', '0037_auto_20150513_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenmedica',
            name='facturada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='farmacia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='medicamento',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='espera',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='espera',
            name='fin',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='espera',
            name='inicio',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
