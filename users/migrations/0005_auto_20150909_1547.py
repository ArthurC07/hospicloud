# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_tipoventa_predeterminada'),
        ('users', '0004_remove_userprofile_persona'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cambio_monetario',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=4),
        ),
        migrations.AddField(
            model_name='company',
            name='chat',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='deposito',
            field=models.ForeignKey(related_name='deposito_company', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='emergencia',
            field=models.ForeignKey(related_name='emergencia_company', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='emergencia_extra',
            field=models.ForeignKey(related_name='emergencia_extra_company', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='help',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='receipt_days',
            field=models.IntegerField(default=30),
        ),
    ]
