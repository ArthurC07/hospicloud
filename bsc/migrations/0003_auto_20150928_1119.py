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
        ('bsc', '0002_auto_20150920_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puntuacion',
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
            model_name='extra',
            name='descripcion',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='extra',
            name='es_puntuado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='extra',
            name='tipo_extra',
            field=models.CharField(default=emergency.models.Emergencia, max_length=3, choices=[(b'ER', 'Emergencias Atendidas'), (b'EV', 'Evaluaci\xf3n del Estudiante')]),
        ),
        migrations.AddField(
            model_name='puntuacion',
            name='extra',
            field=models.ForeignKey(to='bsc.Extra'),
        ),
        migrations.AddField(
            model_name='puntuacion',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
