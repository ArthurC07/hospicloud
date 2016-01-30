# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 17:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aseguradora',
            name='representante',
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='cardex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cardex', to='persona.Persona', verbose_name='Representante'),
        ),
    ]