# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_ciudad_tiene_presupuesto_global'),
        ('contracts', '0038_mastercontract_porcentaje'),
        ('budget', '0011_gasto_factura'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('activo', models.BooleanField(default=True)),
                ('ciudad', models.ForeignKey(to='users.Ciudad')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='gasto',
            name='aseguradora',
            field=models.ForeignKey(blank=True, to='contracts.Aseguradora', null=True),
        ),
    ]
