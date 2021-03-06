# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Cotizacion'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='autorizada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='comprada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='denegada',
            field=models.BooleanField(default=False),
        ),
    ]
