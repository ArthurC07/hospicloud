# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('puntaje_inicial', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('puntaje_final', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('comision', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('tipo_meta', models.CharField(default=b'CT', max_length=3, choices=[(b'CT', 'Tiempo de Consulta'), (b'PCT', 'Tiempo en Preconsulta'), (b'PP', 'Porcentaje de Recetas'), (b'IP', 'Porcentaje de Incapacidades'), (b'CFP', 'Porcentaje de Aprobaci\xf3n del Cliente')])),
                ('peso', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('meta', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('basado_en_tiempo', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ScoreCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='meta',
            name='score_card',
            field=models.ForeignKey(to='bsc.ScoreCard'),
        ),
        migrations.AddField(
            model_name='escala',
            name='score_card',
            field=models.ForeignKey(to='bsc.ScoreCard'),
        ),
    ]
