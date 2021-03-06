# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_auto_20160204_0949'),
        ('clinique', '0006_notamedica'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='espera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consulta_set', to='clinique.Espera'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='poliza',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.MasterContract'),
        ),
        migrations.AddField(
            model_name='espera',
            name='poliza',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.MasterContract'),
        ),
        migrations.AlterField(
            model_name='espera',
            name='fin',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='espera',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
