# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import emergency.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0001_squashed_0045_auto_20150812_1323'),
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
        migrations.AddField(
            model_name='meta',
            name='logro_menor_que_meta',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('tipo_extra', models.CharField(default=emergency.models.Emergencia, max_length=3, choices=[(b'ER', 'Emergencias Atendidas')])),
                ('inicio_de_rango', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('fin_de_rango', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('comision', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('score_card', models.ForeignKey(to='bsc.ScoreCard')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterField(
            model_name='meta',
            name='tipo_meta',
            field=models.CharField(default=b'CT', max_length=3, choices=[(b'CT', 'Tiempo de Consulta'), (b'PCT', 'Tiempo en Preconsulta'), (b'PP', 'Porcentaje de Recetas'), (b'IP', 'Porcentaje de Incapacidades'), (b'CFP', 'Porcentaje de Aprobaci\xf3n del Cliente'), (b'CR', 'Consulta Remitida a Especialista')]),
        ),
        migrations.CreateModel(
            name='Encuesta',
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
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('respuesta', models.CharField(max_length=255)),
                ('valor', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('pregunta', models.CharField(max_length=255)),
                ('valor', models.IntegerField(default=0)),
                ('encuesta', models.ForeignKey(to='bsc.Encuesta')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('consulta', models.ForeignKey(to='clinique.Consulta')),
                ('encuesta', models.ForeignKey(to='bsc.Encuesta')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('opcion', models.ForeignKey(blank=True, to='bsc.Opcion', null=True)),
                ('pregunta', models.ForeignKey(to='bsc.Pregunta')),
                ('respuesta', models.ForeignKey(to='bsc.Respuesta')),
                ('sugerencia', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='opcion',
            name='pregunta',
            field=models.ForeignKey(to='bsc.Pregunta'),
        ),
        migrations.RemoveField(
            model_name='pregunta',
            name='valor',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='calificable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterModelOptions(
            name='pregunta',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='pregunta',
            name='mostrar_sugerencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='terminada',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('day', models.DateField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('holiday', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
