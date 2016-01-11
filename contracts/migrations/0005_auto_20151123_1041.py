# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0017_historiafisica'),
        ('contracts', '0004_auto_20150920_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mastercontract',
            name='vencimiento',
        ),
        migrations.RemoveField(
            model_name='mastercontract',
            name='vida',
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='administrador',
            field=models.ForeignKey(blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='facturar_al_administrador',
            field=models.BooleanField(default=False),
        ),
    ]
