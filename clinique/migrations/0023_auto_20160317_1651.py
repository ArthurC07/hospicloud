# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0022_evaluacion_orl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluacion',
            name='aspecto_general',
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='arritmia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='consciente',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='cuarto_ruido_cardiaco',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='descripcion_cabeza',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='descripcion_cuello',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='descripcion_ojos',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='lucido',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='orientado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='primer_ruido_cardiaco',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='segundo_ruido_cardiaco',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='soplo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='tercer_ruido_cardiaco',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='cabeza',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Anormal')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='cardiopulmonar',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='cuello',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Anormal')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='descripcion_orl',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='extremidades',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='gastrointestinal',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='ojos',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Anormal')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='orl',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Anormal')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='otras',
            field=models.TextField(blank=True),
        ),
    ]