# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import decimal
import django_extensions.db.fields


class Migration(migrations.Migration):

    replaces = [(b'budget', '0001_initial'), (b'budget', '0002_presupuesto_activo'), (b'budget', '0003_auto_20150722_0923'), (b'budget', '0004_gasto_comprobante'), (b'budget', '0005_presupuesto_porcentaje_global'), (b'budget', '0006_auto_20150731_1100'), (b'budget', '0007_gasto_fecha_de_pago'), (b'budget', '0008_gasto_periodo_de_pago'), (b'budget', '0009_auto_20150731_1142'), (b'budget', '0010_presupuesto_inversion'), (b'budget', '0011_gasto_factura'), (b'budget', '0012_auto_20150814_1108'), (b'budget', '0013_auto_20150826_1801'), (b'budget', '0014_gasto_comprobante_entregado'), (b'budget', '0015_auto_20150907_0925')]

    dependencies = [
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        ('contracts', '0001_squashed_0039_auto_20150817_0933'),
        ('users', '0001_squashed_0011_ciudad_tiene_presupuesto_global'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255)),
                ('limite', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField()),
                ('monto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('cuenta', models.ForeignKey(to='budget.Cuenta')),
                ('cheque', models.CharField(max_length=255, null=True, blank=True)),
                ('proveedor', models.ForeignKey(blank=True, to='inventory.Proveedor', null=True)),
                ('comprobante', models.FileField(null=True, upload_to=b'budget/gasto/%Y/%m/%d', blank=True)),
                ('ejecutado', models.BooleanField(default=False)),
                ('fecha_maxima_de_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_de_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('periodo_de_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('factura', models.CharField(max_length=255, null=True, blank=True)),
                ('aseguradora', models.ForeignKey(blank=True, to='contracts.Aseguradora', null=True)),
                ('numero_pagos', models.IntegerField(default=1)),
                ('proximo_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('comprobante_entregado', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('ciudad', models.ForeignKey(to='users.Ciudad')),
                ('activo', models.BooleanField(default=True)),
                ('porcentaje_global', models.DecimalField(default=decimal.Decimal, max_digits=3, decimal_places=2)),
                ('inversion', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='cuenta',
            name='presupuesto',
            field=models.ForeignKey(to='budget.Presupuesto'),
        ),
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
        migrations.AlterModelOptions(
            name='cuenta',
            options={'ordering': ('nombre',)},
        ),
        migrations.CreateModel(
            name='Fuente',
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
            model_name='gasto',
            name='fuente',
            field=models.ForeignKey(blank=True, to='budget.Fuente', null=True),
        ),
    ]
