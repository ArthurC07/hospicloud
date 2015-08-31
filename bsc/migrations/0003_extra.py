# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import emergency.models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0002_meta_logro_menor_que_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('tipo_extra', models.CharField(default=emergency.models.Emergencia, max_length=3, choices=[(emergency.models.Emergencia, 'Emergencias Atendidas')])),
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
    ]
