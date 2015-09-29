# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bsc', '0003_auto_20150928_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('puntaje', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='meta',
            name='activa',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='meta',
            name='tipo_meta',
            field=models.CharField(default=b'CT', max_length=3, choices=[(b'CT', 'Tiempo de Consulta'), (b'PCT', 'Tiempo en Preconsulta'), (b'PP', 'Porcentaje de Recetas'), (b'IP', 'Porcentaje de Incapacidades'), (b'CFP', 'Porcentaje de Aprobaci\xf3n del Cliente'), (b'CR', 'Consulta Remitida a Especialista'), (b'CO', 'Coaching'), (b'PU', 'Puntualidad'), (b'QJ', 'Manejo de Quejas')]),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='meta',
            field=models.ForeignKey(to='bsc.Meta'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
