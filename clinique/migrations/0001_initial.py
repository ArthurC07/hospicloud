# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 15:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persona', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Afeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('cantidad', models.IntegerField(default=1)),
                ('facturado', models.BooleanField(default=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('ausente', models.BooleanField(default=False)),
                ('atendida', models.BooleanField(default=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('motivo_de_consulta', models.TextField(default=None, null=True)),
                ('HEA', models.TextField(default=None, null=True)),
                ('facturada', models.BooleanField(default=False)),
                ('activa', models.BooleanField(default=True)),
                ('final', models.DateTimeField(blank=True, null=True)),
                ('remitida', models.BooleanField(default=False)),
                ('encuestada', models.BooleanField(default=False)),
                ('revisada', models.BooleanField(default=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('especialista', models.BooleanField(default=False)),
                ('administradores', models.ManyToManyField(blank=True, related_name='consultorios_administrados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['nombre'],
                'permissions': (('consultorio', 'Permite al usuario gestionar consultorios'),),
            },
        ),
        migrations.CreateModel(
            name='DiagnosticoClinico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('diagnostico', models.TextField(blank=True, null=True)),
                ('afeccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos_clinicos', to='clinique.Afeccion')),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos_clinicos', to='clinique.Consulta')),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos_clinicos', to='persona.Persona')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosticos_clinicos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(max_length=50)),
                ('habilitado', models.BooleanField(default=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('atendido', models.BooleanField(default=False)),
                ('ausente', models.BooleanField(default=False)),
                ('consulta', models.BooleanField(default=False)),
                ('inicio', models.DateTimeField(auto_now_add=True)),
                ('terminada', models.BooleanField(default=False)),
                ('fin', models.DateTimeField(auto_now_add=True)),
                ('consultorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='espera', to='clinique.Consultorio')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espera', to='persona.Persona')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('orl', models.TextField()),
                ('cardiopulmonar', models.TextField()),
                ('gastrointestinal', models.TextField()),
                ('extremidades', models.TextField()),
                ('otras', models.TextField()),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='clinique.Consulta')),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to='persona.Persona')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluaciones', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('descripcion', models.TextField()),
                ('dias', models.IntegerField(default=0)),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incapacidades', to='clinique.Consulta')),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incapacidades', to='persona.Persona')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incapacidades', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('pulso', models.IntegerField()),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('presion_sistolica', models.IntegerField(null=True)),
                ('presion_diastolica', models.IntegerField(null=True)),
                ('respiracion', models.IntegerField(null=True)),
                ('presion_arterial_media', models.CharField(blank=True, max_length=200)),
                ('persona', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lecturas_signos', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('habilitado', models.BooleanField(default=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nota', models.TextField(blank=True)),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notas_enfermeria', to='persona.Persona')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultorio_notas_enfermeria', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('orden', models.TextField(blank=True)),
                ('farmacia', models.BooleanField(default=False)),
                ('facturada', models.BooleanField(default=False)),
                ('consulta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordenes_medicas', to='clinique.Consulta')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordenes_clinicas', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('consultorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='clinique.Consultorio')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='persona.Persona')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('dosis', models.TextField(blank=True, null=True)),
                ('medicamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescripciones', to='inventory.ItemTemplate')),
                ('orden', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinique.OrdenMedica')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Remision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('motivo', models.TextField()),
                ('consultorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remisiones', to='clinique.Consultorio')),
                ('especialidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='remisiones', to='clinique.Especialidad')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remisiones', to='persona.Persona')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archivo', models.FileField(upload_to=b'consultorio/reports/%Y/%m/%d')),
                ('fecha', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('consultorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='clinique.Consultorio')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('observaciones', models.TextField()),
                ('consultorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to='clinique.Consultorio')),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to='persona.Persona')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguimientos', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(blank=True, max_length=200)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('habilitado', models.BooleanField(default=True)),
                ('facturable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoRemision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remisiones', to='clinique.TipoRemision'),
        ),
        migrations.AddField(
            model_name='examen',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultorio_examenes', to='clinique.Paciente'),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultorios', to='clinique.Especialidad'),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='inventario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultorios', to='inventory.Inventario'),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='localidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultorios', to='clinique.Localidad'),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='secretaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secretarias', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultorio',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultorios', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consulta',
            name='consultorio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='clinique.Consultorio'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='clinique.TipoConsulta'),
        ),
        migrations.AddField(
            model_name='cita',
            name='consultorio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='clinique.Consultorio'),
        ),
        migrations.AddField(
            model_name='cita',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='consulta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='clinique.Consulta'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultorio_cargos', to='inventory.ItemTemplate'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='inventory.ItemType'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cargos_clinicos', to=settings.AUTH_USER_MODEL),
        ),
    ]