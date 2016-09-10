# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-27 05:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0012_persona_cargo'),
        ('clinique', '0026_ordenlaboratorio_ordenlaboratorioitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaFisicaEspera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='espera',
            name='datos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='espera',
            name='duracion_total',
            field=models.DurationField(default=datetime.timedelta),
        ),
        migrations.AddField(
            model_name='espera',
            name='fin_consultorio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='fin_datos',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='fin_enfermeria',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='fin_sap',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio_datos',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio_doctor',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio_enfermeria',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio_sap',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='tiempo_consultorio',
            field=models.DurationField(default=datetime.timedelta),
        ),
        migrations.AddField(
            model_name='espera',
            name='tiempo_datos',
            field=models.DurationField(default=datetime.timedelta),
        ),
        migrations.AddField(
            model_name='espera',
            name='tiempo_enfermeria',
            field=models.DurationField(default=datetime.timedelta),
        ),
        migrations.AddField(
            model_name='espera',
            name='tiempo_sap',
            field=models.DurationField(default=datetime.timedelta),
        ),
        migrations.AddField(
            model_name='historiafisicaespera',
            name='espera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinique.Espera'),
        ),
        migrations.AddField(
            model_name='historiafisicaespera',
            name='historia_fisica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.HistoriaFisica'),
        ),
    ]
