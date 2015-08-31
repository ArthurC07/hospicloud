# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('persona', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('emergency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('momento', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('diagnostico', models.CharField(max_length=200, blank=True)),
                ('doctor', models.CharField(max_length=200, blank=True)),
                ('arancel', models.CharField(blank=True, max_length=200, choices=[(b'E', 'Empleado'), (b'J', 'Ejecutivo'), (b'X', 'Extranjero')])),
                ('pago', models.CharField(blank=True, max_length=200, choices=[(b'EF', 'Efectivo'), (b'CK', 'Cheque'), (b'CO', 'Empresa'), (b'OC', 'Orden de Compra'), (b'TC', 'Tarjeta Cr\xe9dito'), (b'TB', 'Transferencia Bancaria')])),
                ('poliza', models.CharField(max_length=200, blank=True)),
                ('certificado', models.CharField(max_length=200, blank=True)),
                ('aseguradora', models.CharField(max_length=200, blank=True)),
                ('deposito', models.CharField(max_length=200, blank=True)),
                ('observaciones', models.CharField(max_length=200, blank=True)),
                ('admision', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('autorizacion', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('hospitalizacion', models.DateTimeField(null=True, blank=True)),
                ('ingreso', models.DateTimeField(null=True, blank=True)),
                ('fecha_pago', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('fecha_alta', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('estado', models.CharField(blank=True, max_length=1, choices=[(b'A', b'Admitido'), (b'B', b'Autorizado'), (b'H', b'Hospitalizar'), (b'I', b'Ingresado'), (b'C', b'Alta'), (b'Q', b'Cancelada')])),
                ('tiempo', models.IntegerField(default=0, blank=True)),
                ('neonato', models.NullBooleanField()),
                ('tipo_de_ingreso', models.CharField(blank=True, max_length=200, null=True, choices=[(b'PA', b'Particular'), (b'SN', b'Aseguradora Nacional'), (b'SI', b'Aseguradora Internacional'), (b'PS', b'Presupuesto')])),
                ('facturada', models.NullBooleanField(default=False)),
                ('ultimo_cobro', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('admitio', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('fiadores', models.ManyToManyField(related_name='fianzas', null=True, to='persona.Persona', blank=True)),
            ],
            options={
                'permissions': (('admision', 'Permite al usuario gestionar admision'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('recibo', models.IntegerField(null=True, blank=True)),
                ('admision', models.ForeignKey(related_name='depositos', to='spital.Admision')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('tipo', models.CharField(blank=True, max_length=1, choices=[(b'N', b'Normal'), (b'S', b'Suite'), (b'U', b'U.C.I.')])),
                ('estado', models.CharField(blank=True, max_length=1, choices=[(b'D', b'Disponible'), (b'O', b'Ocupada'), (b'M', b'Mantenimiento')])),
                ('item', models.ForeignKey(related_name='habitaciones', blank=True, to='inventory.ItemTemplate', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreAdmision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('completada', models.BooleanField(default=False)),
                ('transferir_cobros', models.BooleanField(default=False)),
                ('emergencia', models.ForeignKey(related_name='preadmisiones', to='emergency.Emergencia')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='admision',
            name='habitacion',
            field=models.ForeignKey(related_name='admisiones', blank=True, to='spital.Habitacion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='admision',
            name='paciente',
            field=models.ForeignKey(related_name='admisiones', to='persona.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='admision',
            name='referencias',
            field=models.ManyToManyField(related_name='referencias', null=True, to='persona.Persona', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='admision',
            name='tipo_de_venta',
            field=models.ForeignKey(blank=True, to='inventory.TipoVenta', null=True),
            preserve_default=True,
        ),
    ]
