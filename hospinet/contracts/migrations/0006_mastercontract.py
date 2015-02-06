# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
        ('contracts', '0005_aseguradora_beneficio'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicio', models.DateField(default=django.utils.timezone.now)),
                ('vencimiento', models.DateField(default=django.utils.timezone.now)),
                ('archivo', models.FileField(null=True, upload_to=b'contracts/csv//%Y/%m/%d', blank=True)),
                ('aseguradora', models.ForeignKey(related_name='master_contracts', to='contracts.Aseguradora')),
                ('contratante', models.ForeignKey(related_name='master_contracts', blank=True, to='persona.Empleador', null=True)),
                ('plan', models.ForeignKey(related_name='master_contracts', to='contracts.Plan')),
                ('vendedor', models.ForeignKey(related_name='master_contracts', to='contracts.Vendedor')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
    ]
