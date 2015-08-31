# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nightingale.models
import django_extensions.db.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.DecimalField(default=1, max_digits=8, decimal_places=2)),
                ('facturada', models.NullBooleanField(default=False)),
                ('admision', models.ForeignKey(related_name='cargos', to='spital.Admision')),
                ('cargo', models.ForeignKey(related_name='cargos', blank=True, to='inventory.ItemTemplate', null=True)),
                ('usuario', models.ForeignKey(related_name='cargos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'permissions': (('enfermeria', 'Permite al usuario gestionar hospitalizaciones'), ('enfermeria_ver', 'Permite al usuario ver datos')),
            },
            bases=(models.Model, nightingale.models.Precio),
        ),
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField(max_length=200, null=True, blank=True)),
                ('admision', models.ForeignKey(related_name='devoluciones', to='spital.Admision')),
                ('cargo', models.ForeignKey(related_name='devoluciones', blank=True, to='inventory.ItemTemplate', null=True)),
                ('usuario', models.ForeignKey(related_name='devoluciones', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Dosis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('estado', models.IntegerField(default=1, null=True, blank=True, choices=[(1, 'Pendiente'), (2, 'Rechazada'), (3, 'Administrada')])),
                ('recomendacion', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Evolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('nota', models.TextField(blank=True)),
                ('admision', models.ForeignKey(related_name='evoluciones', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='evoluciones', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Excreta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('medio', models.CharField(blank=True, max_length=2, choices=[(b'S', 'Succi\xf3n'), (b'O', b'Orina'), (b'V', b'Vomito')])),
                ('cantidad', models.CharField(max_length=200, blank=True)),
                ('descripcion', models.CharField(max_length=200, blank=True)),
                ('otro', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
                ('admision', models.ForeignKey(related_name='excretas', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='excretas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='FrecuenciaLectura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('glucometria', models.IntegerField(default=0, blank=True)),
                ('signos_vitales', models.IntegerField(default=0, blank=True)),
                ('admision', models.OneToOneField(to='spital.Admision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Glicemia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('control', models.CharField(max_length=200, blank=True)),
                ('observacion', models.CharField(max_length=200, blank=True)),
                ('admision', models.ForeignKey(related_name='glicemias', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='glicemias', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Glucosuria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('control', models.CharField(max_length=200, blank=True)),
                ('observacion', models.TextField(blank=True)),
                ('admision', models.ForeignKey(related_name='glucosurias', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='glucosurias', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Honorario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('medico', models.CharField(max_length=200, blank=True)),
                ('facturada', models.NullBooleanField(default=False)),
                ('admision', models.ForeignKey(related_name='honorarios', to='spital.Admision')),
                ('item', models.ForeignKey(related_name='honorarios', blank=True, to='inventory.ItemTemplate', null=True)),
                ('usuario', models.ForeignKey(related_name='honorarios', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('ingerido', models.CharField(max_length=200, blank=True)),
                ('cantidad', models.IntegerField()),
                ('liquido', models.NullBooleanField()),
                ('via', models.CharField(max_length=200, null=True, blank=True)),
                ('admision', models.ForeignKey(related_name='ingestas', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='ingestas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Insulina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('control', models.CharField(max_length=200, blank=True)),
                ('observacion', models.CharField(max_length=200, blank=True)),
                ('admision', models.ForeignKey(related_name='insulina', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='insulinas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('intervalo', models.IntegerField(blank=True, null=True, choices=[(24, 'Cada 24 Horas'), (12, 'Cada 12 Horas'), (8, 'Cada 8 Horas'), (6, 'Cada 6 Horas'), (4, 'Cada 4 Horas')])),
                ('unidades', models.CharField(max_length=200, blank=True)),
                ('repeticiones', models.IntegerField(null=True, blank=True)),
                ('estado', models.IntegerField(default=1, null=True, blank=True, choices=[(1, 'Activo'), (2, 'Suspendido'), (3, 'Terminado')])),
                ('ultima_dosis', models.DateTimeField(default=django.utils.timezone.now)),
                ('proxima_dosis', models.DateTimeField(default=django.utils.timezone.now)),
                ('suministrado', models.IntegerField(default=0)),
                ('admision', models.ForeignKey(related_name='medicamentos', to='spital.Admision')),
                ('cargo', models.ForeignKey(related_name='medicamentos', blank=True, to='inventory.ItemTemplate', null=True)),
                ('usuario', models.ForeignKey(related_name='medicamentos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotaEnfermeria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('nota', models.TextField(blank=True)),
                ('autor', models.CharField(max_length=200, blank=True)),
                ('cerrada', models.BooleanField(default=False)),
                ('admision', models.ForeignKey(related_name='notas_enfermeria', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='notas_enfermeria', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='OrdenMedica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evolucion', models.TextField(blank=True)),
                ('orden', models.TextField(blank=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('doctor', models.CharField(max_length=255, null=True, blank=True)),
                ('admision', models.ForeignKey(related_name='ordenes_medicas', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='ordenes_medicas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OxigenoTerapia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('terminada', models.BooleanField(default=False)),
                ('inicio', models.DateTimeField(null=True, blank=True)),
                ('fin', models.DateTimeField(null=True, blank=True)),
                ('facturada', models.NullBooleanField(default=False)),
                ('admision', models.ForeignKey(related_name='oxigeno_terapias', to='spital.Admision')),
                ('cargo', models.ForeignKey(related_name='oxigeno_terapias', blank=True, to='inventory.ItemTemplate', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model, nightingale.models.Precio),
        ),
        migrations.CreateModel(
            name='SignoVital',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_y_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('pulso', models.IntegerField()),
                ('temperatura', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_sistolica', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_diastolica', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('respiracion', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('saturacion_de_oxigeno', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_arterial_media', models.CharField(max_length=200, blank=True)),
                ('admision', models.ForeignKey(related_name='signos_vitales', to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='signos_vitales', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model, nightingale.models.Turno),
        ),
        migrations.CreateModel(
            name='Sumario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('diagnostico', models.TextField(blank=True)),
                ('procedimiento_efectuado', models.TextField(blank=True)),
                ('condicion', models.TextField(blank=True)),
                ('recomendaciones', models.TextField(blank=True)),
                ('fecha', models.DateTimeField(null=True, blank=True)),
                ('admision', models.OneToOneField(to='spital.Admision')),
                ('usuario', models.ForeignKey(related_name='sumarios', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dosis',
            name='medicamento',
            field=models.ForeignKey(related_name='dosis', to='nightingale.Medicamento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dosis',
            name='usuario',
            field=models.ForeignKey(related_name='dosis', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
