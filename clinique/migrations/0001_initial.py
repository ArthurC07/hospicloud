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
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField(default=1)),
                ('item', models.ForeignKey(related_name='consultorio_cargos', to='inventory.ItemTemplate')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('ausente', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('administradores', models.ManyToManyField(related_name='consultorios_administrados', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('inventario', models.ForeignKey(related_name='consultorios', blank=True, to='inventory.Inventario', null=True)),
                ('secretaria', models.ForeignKey(related_name='secretarias', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(related_name='consultorios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('consultorio', 'Permite al usuario gestionar consultorios'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiagnosticoClinico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('diagnostico', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Espera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('atendido', models.BooleanField(default=False)),
                ('ausente', models.BooleanField(default=False)),
                ('consultorio', models.ForeignKey(related_name='espera', blank=True, to='clinique.Consultorio', null=True)),
                ('persona', models.ForeignKey(related_name='espera', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('orl', models.TextField()),
                ('cardiopulmonar', models.TextField()),
                ('gastrointestinal', models.TextField()),
                ('extremidades', models.TextField()),
                ('otras', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField(blank=True)),
                ('adjunto', models.FileField(upload_to=b'clinique/examen/%Y/%m/%d')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incapacidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField()),
                ('consultorio', models.ForeignKey(related_name='incapacidades', to='clinique.Consultorio')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LecturaSignos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('pulso', models.IntegerField()),
                ('temperatura', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_sistolica', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_diastolica', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('respiracion', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_arterial_media', models.CharField(max_length=200, blank=True)),
                ('persona', models.ForeignKey(related_name='lecturas_signos', to='persona.Persona', null=True)),
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
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nota', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrdenMedica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('evolucion', models.TextField(blank=True)),
                ('orden', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('consultorio', models.ForeignKey(related_name='pacientes', blank=True, to='clinique.Consultorio', null=True)),
                ('persona', models.ForeignKey(related_name='pacientes', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prescripcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nota', models.TextField(blank=True)),
                ('paciente', models.ForeignKey(related_name='prescripciones', to='clinique.Paciente')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('archivo', models.FileField(upload_to=b'consultorio/reports/%Y/%m/%d')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('consultorio', models.ForeignKey(related_name='reportes', blank=True, to='clinique.Consultorio', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('observaciones', models.TextField()),
                ('paciente', models.ForeignKey(related_name='seguimientos', to='clinique.Paciente')),
                ('usuario', models.ForeignKey(related_name='seguimientos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoCargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=200, blank=True)),
                ('descontable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoConsulta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='paciente',
            field=models.ForeignKey(related_name='ordenes_medicas', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='paciente',
            field=models.ForeignKey(related_name='notas_enfermeria', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='usuario',
            field=models.ForeignKey(related_name='consultorio_notas_enfermeria', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='paciente',
            field=models.ForeignKey(related_name='incapacidades', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examen',
            name='paciente',
            field=models.ForeignKey(related_name='consultorio_examenes', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='paciente',
            field=models.ForeignKey(related_name='evaluaciones', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='paciente',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(related_name='consultas', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consulta',
            name='tipo',
            field=models.ForeignKey(related_name='consultas', to='clinique.TipoConsulta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cita',
            name='consultorio',
            field=models.ForeignKey(related_name='citas', blank=True, to='clinique.Consultorio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cita',
            name='persona',
            field=models.ForeignKey(related_name='citas', blank=True, to='persona.Persona', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cargo',
            name='paciente',
            field=models.ForeignKey(related_name='cargos', to='clinique.Paciente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cargo',
            name='tipo',
            field=models.ForeignKey(related_name='cargos', to='clinique.TipoCargo'),
            preserve_default=True,
        ),
    ]
