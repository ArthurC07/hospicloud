# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CierreTurno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('comprobante', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('remite', models.CharField(max_length=255, null=True, blank=True)),
                ('radiologo', models.CharField(max_length=255, null=True, blank=True)),
                ('discount', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('cerrado', models.BooleanField(default=False)),
                ('nulo', models.BooleanField(default=False)),
                ('cajero', models.ForeignKey(related_name='recibos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('cliente', models.ForeignKey(related_name='recibos', to='persona.Persona')),
                ('tipo_de_venta', models.ForeignKey(blank=True, to='inventory.TipoVenta', null=True)),
            ],
            options={
                'permissions': (('cajero', 'Permite al usuario gestionar caja'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurnoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicio', models.DateTimeField(null=True, blank=True)),
                ('fin', models.DateTimeField(null=True, blank=True)),
                ('apertura', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('finalizado', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(related_name='turno_caja', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('precio', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('impuesto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('descuento', models.IntegerField(default=0)),
                ('placas', models.IntegerField(default=0)),
                ('descontable', models.BooleanField(default=True)),
                ('item', models.ForeignKey(related_name='ventas', blank=True, to='inventory.ItemTemplate', null=True)),
                ('recibo', models.ForeignKey(related_name='ventas', to='invoice.Recibo')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pago',
            name='recibo',
            field=models.ForeignKey(related_name='pagos', to='invoice.Recibo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pago',
            name='tipo',
            field=models.ForeignKey(related_name='pagos', to='invoice.TipoPago'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cierreturno',
            name='pago',
            field=models.ForeignKey(related_name='cierres', to='invoice.TipoPago'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cierreturno',
            name='turno',
            field=models.ForeignKey(related_name='cierres', to='invoice.TurnoCaja'),
            preserve_default=True,
        ),
    ]
