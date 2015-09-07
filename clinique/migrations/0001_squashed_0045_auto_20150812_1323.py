# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import django.utils.timezone
from django.conf import settings


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# clinique.migrations.0021_auto_20150426_2011
# clinique.migrations.0015_auto_20150424_1637
# clinique.migrations.0029_auto_20150429_1707
# clinique.migrations.0024_diagnosticoclinico_usuario


def update_diagnostico_user(apps, schema_editor):

    DiagnosticoClinico = apps.get_model("clinique", "DiagnosticoClinico")

    for diagnostico in DiagnosticoClinico.objects.all():
        diagnostico.usuario = diagnostico.consultorio.usuario
        diagnostico.save()


def update_incapacidad_user(apps, schema_editor):
    Incapacidad = apps.get_model("clinique", "Incapacidad")

    for incapacidad in Incapacidad.objects.all():

        incapacidad.usuario = incapacidad.consultorio.usuario
        incapacidad.save()


def extract_user(apps, schema_editor):

    OrdenMedica = apps.get_model("clinique", "OrdenMedica")

    for orden in OrdenMedica.objects.all():
        orden.usuario = orden.consultorio.usuario
        orden.save()


def expand_paciente(apps, schema_editor):
    Consulta = apps.get_model("clinique", "Consulta")

    for consulta in Consulta.objects.all():
        consulta.persona = consulta.paciente.persona
        consulta.consultorio = consulta.paciente.consultorio
        consulta.save()

    Evaluacion = apps.get_model("clinique", "Evaluacion")

    for evaluacion in Evaluacion.objects.all():
        evaluacion.persona = evaluacion.paciente.persona
        evaluacion.consultorio = evaluacion.paciente.consultorio
        evaluacion.save()

    Seguimiento = apps.get_model("clinique", "Seguimiento")

    for seguimiento in Seguimiento.objects.all():
        seguimiento.persona = seguimiento.paciente.persona
        seguimiento.consultorio = seguimiento.paciente.consultorio
        seguimiento.save()

    DiagnosticoClinico = apps.get_model("clinique", "DiagnosticoClinico")

    for diagnostico in DiagnosticoClinico.objects.all():
        diagnostico.persona = diagnostico.paciente.persona
        diagnostico.consultorio = diagnostico.paciente.consultorio
        diagnostico.save()

    OrdenMedica = apps.get_model("clinique", "OrdenMedica")

    for orden in OrdenMedica.objects.all():
        orden.persona = orden.paciente.persona
        orden.consultorio = orden.paciente.consultorio
        orden.save()

    Cargo = apps.get_model("clinique", "Cargo")

    for cargo in Cargo.objects.all():
        cargo.persona = cargo.paciente.persona
        cargo.consultorio = cargo.paciente.consultorio
        cargo.save()

    NotaEnfermeria = apps.get_model("clinique", "NotaEnfermeria")

    for nota in NotaEnfermeria.objects.all():
        nota.persona = nota.paciente.persona
        nota.consultorio = nota.paciente.consultorio
        nota.save()

    Prescripcion = apps.get_model("clinique", "Prescripcion")

    for prescripcion in Prescripcion.objects.all():
        prescripcion.persona = prescripcion.paciente.persona
        prescripcion.consultorio = prescripcion.paciente.consultorio
        prescripcion.save()

    Incapacidad = apps.get_model("clinique", "Incapacidad")

    for incapacidad in Incapacidad.objects.all():
        incapacidad.persona = incapacidad.paciente.persona
        incapacidad.consultorio = incapacidad.paciente.consultorio
        incapacidad.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150507_1637'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
        ('inventory', '0009_remove_historial_fecha'),
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
        ),
        migrations.CreateModel(
            name='LecturaSignos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('pulso', models.IntegerField()),
                ('temperatura', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('presion_sistolica', models.IntegerField(null=True)),
                ('presion_diastolica', models.IntegerField(null=True)),
                ('respiracion', models.IntegerField(null=True)),
                ('presion_arterial_media', models.CharField(max_length=200, blank=True)),
                ('persona', models.ForeignKey(related_name='lecturas_signos', to='persona.Persona', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
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
        ),
        migrations.CreateModel(
            name='TipoConsulta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=50)),
                ('habilitado', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='paciente',
            field=models.ForeignKey(related_name='ordenes_medicas', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='paciente',
            field=models.ForeignKey(related_name='notas_enfermeria', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='usuario',
            field=models.ForeignKey(related_name='consultorio_notas_enfermeria', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='paciente',
            field=models.ForeignKey(related_name='incapacidades', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='examen',
            name='paciente',
            field=models.ForeignKey(related_name='consultorio_examenes', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='paciente',
            field=models.ForeignKey(related_name='evaluaciones', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='paciente',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(related_name='consultas', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='tipo',
            field=models.ForeignKey(related_name='consultas', to='clinique.TipoConsulta'),
        ),
        migrations.AddField(
            model_name='cita',
            name='consultorio',
            field=models.ForeignKey(related_name='citas', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='cita',
            name='persona',
            field=models.ForeignKey(related_name='citas', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='paciente',
            field=models.ForeignKey(related_name='cargos', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='tipo',
            field=models.ForeignKey(related_name='cargos', to='inventory.ItemType'),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='motivo_de_consulta',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='HEA',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='cita',
            name='atendida',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='dias',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='consultorio',
            name='localidad',
            field=models.ForeignKey(related_name='consultorios', blank=True, to='clinique.Localidad', null=True),
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='consultorio',
            name='especialidad',
            field=models.ForeignKey(related_name='consultorios', blank=True, to='clinique.Especialidad', null=True),
        ),
        migrations.CreateModel(
            name='Remision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('motivo', models.TextField()),
                ('consultorio', models.ForeignKey(related_name='remisiones', to='clinique.Consultorio')),
                ('especialidad', models.ForeignKey(related_name='remisiones', blank=True, to='clinique.Especialidad', null=True)),
                ('persona', models.ForeignKey(related_name='remisiones', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='TipoRemision',
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
        ),
        migrations.AddField(
            model_name='remision',
            name='tipo',
            field=models.ForeignKey(related_name='remisiones', to='clinique.TipoRemision'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='facturado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consulta',
            name='activa',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='facturada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='consulta',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='consultorio',
            field=models.ForeignKey(related_name='cargos', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='persona',
            field=models.ForeignKey(related_name='cargos', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='consultorio',
            field=models.ForeignKey(related_name='consultas', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='final',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='persona',
            field=models.ForeignKey(related_name='consultas', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='consultorio',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='persona',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='consultorio',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='persona',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='persona',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='consultorio',
            field=models.ForeignKey(related_name='notas_enfermeria', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='notaenfermeria',
            name='persona',
            field=models.ForeignKey(related_name='notas_enfermeria', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='consultorio',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='persona',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='consultorio',
            field=models.ForeignKey(related_name='seguimientos', blank=True, to='clinique.Consultorio', null=True),
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='persona',
            field=models.ForeignKey(related_name='seguimientos', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='persona',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='persona.Persona', null=True),
        ),
        migrations.RunPython(
            code=expand_paciente,
        ),
        migrations.RemoveField(
            model_name='cargo',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='diagnosticoclinico',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='incapacidad',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='notaenfermeria',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='seguimiento',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='notaenfermeria',
            name='consultorio',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='consultorio',
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='usuario',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='consulta',
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='usuario',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RunPython(
            code=update_incapacidad_user,
        ),
        migrations.RemoveField(
            model_name='incapacidad',
            name='consultorio',
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='usuario',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='usuario',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RunPython(
            code=update_diagnostico_user,
        ),
        migrations.RemoveField(
            model_name='diagnosticoclinico',
            name='consultorio',
        ),
        migrations.AddField(
            model_name='espera',
            name='consulta',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='espera',
            name='fin',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='espera',
            name='terminada',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelOptions(
            name='consultorio',
            options={'ordering': ['nombre'], 'permissions': (('consultorio', 'Permite al usuario gestionar consultorios'),)},
        ),
        migrations.RemoveField(
            model_name='cargo',
            name='consultorio',
        ),
        migrations.RemoveField(
            model_name='cargo',
            name='persona',
        ),
        migrations.AddField(
            model_name='cargo',
            name='consulta',
            field=models.ForeignKey(related_name='cargos', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='usuario',
            field=models.ForeignKey(related_name='cargos_clinicos', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='usuario',
            field=models.ForeignKey(related_name='ordenes_clinicas', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.RunPython(
            code=extract_user,
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='consultorio',
        ),
        migrations.CreateModel(
            name='Afeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='afeccion',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Afeccion', null=True),
        ),
        migrations.AddField(
            model_name='tipoconsulta',
            name='facturable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='consulta',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AddField(
            model_name='incapacidad',
            name='consulta',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='consulta',
            field=models.ForeignKey(related_name='ordenes_medicas', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='consulta',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Consulta', null=True),
        ),
        migrations.AlterField(
            model_name='diagnosticoclinico',
            name='diagnostico',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='consultorio',
            name='administradores',
            field=models.ManyToManyField(related_name='consultorios_administrados', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='medicamento',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='nota',
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='facturada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ordenmedica',
            name='farmacia',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='espera',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='espera',
            name='fin',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='espera',
            name='inicio',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='remitida',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='evolucion',
        ),
        migrations.AddField(
            model_name='consulta',
            name='encuestada',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='persona',
        ),
        migrations.RemoveField(
            model_name='prescripcion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='orden',
            field=models.ForeignKey(blank=True, to='clinique.OrdenMedica', null=True),
        ),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='persona',
        ),
        migrations.AddField(
            model_name='prescripcion',
            name='dosis',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='revisada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='especialista',
            field=models.BooleanField(default=False),
        ),
    ]
