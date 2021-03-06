# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 15:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import persona.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntecedenteQuirurgico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('procedimiento', models.CharField(blank=True, max_length=200)),
                ('fecha', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Empleador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('nombre', models.CharField(blank=True, max_length=200)),
                ('direccion', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Empleo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('numero_empleado', models.CharField(blank=True, max_length=200, null=True)),
                ('empleador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleos', to='persona.Empleador')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='HistoriaFisica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tipo_identificacion', models.CharField(blank=True, choices=[(b'R', 'Carnet de Residencia'), (b'L', 'Licencia'), (b'P', 'Pasaporte'), (b'T', 'Tarjeta de Identidad'), (b'N', 'Ninguno')], max_length=1)),
                ('identificacion', models.CharField(blank=True, max_length=20)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellido', models.CharField(blank=True, max_length=50)),
                ('sexo', models.CharField(blank=True, choices=[(b'M', 'Masculino'), (b'F', 'Femenino')], max_length=1)),
                ('nacimiento', models.DateField(default=datetime.date.today)),
                ('estado_civil', models.CharField(blank=True, choices=[(b'S', 'Soltero/a'), (b'D', 'Divorciado/a'), (b'C', 'Casado/a'), (b'U', 'Union Libre')], max_length=1)),
                ('profesion', models.CharField(blank=True, max_length=200)),
                ('telefono', models.CharField(blank=True, max_length=200)),
                ('celular', models.CharField(blank=True, max_length=200)),
                ('domicilio', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('fax', models.CharField(blank=True, max_length=200)),
                ('fotografia', models.ImageField(blank=True, help_text=b'El archivo debe estar en formato jpg o png y no pesar mas de 120kb', null=True, upload_to=b'persona/foto//%Y/%m/%d')),
                ('nacionalidad', persona.fields.OrderedCountryField(blank=True, max_length=2)),
                ('duplicado', models.BooleanField(default=False)),
                ('rtn', models.CharField(blank=True, max_length=200, null=True)),
                ('mostrar_en_cardex', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('persona', 'Permite al usuario gestionar persona'),),
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('lugar', models.CharField(blank=True, max_length=200)),
                ('direccion', models.TextField()),
                ('empleador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sedes', to='persona.Empleador')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='persona.Persona')),
                ('cardiopatia', models.BooleanField(default=False)),
                ('hipertension', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('hepatitis', models.BooleanField(default=False)),
                ('rinitis', models.BooleanField(default=False)),
                ('tuberculosis', models.BooleanField(default=False)),
                ('artritis', models.BooleanField(default=False)),
                ('asma', models.BooleanField(default=False)),
                ('colitis', models.BooleanField(default=False)),
                ('gastritis', models.BooleanField(default=False)),
                ('sinusitis', models.BooleanField(default=False)),
                ('hipertrigliceridemia', models.BooleanField(default=False)),
                ('colelitiasis', models.BooleanField(default=False)),
                ('migrana', models.BooleanField(default=False, verbose_name='Migra\xf1a')),
                ('obesidad', models.BooleanField(default=False)),
                ('colesterol', models.BooleanField(default=False)),
                ('trigliceridos', models.BooleanField(default=False)),
                ('alcoholismo', models.BooleanField(default=False)),
                ('cancer', models.BooleanField(default=False)),
                ('tiroides', models.BooleanField(default=False)),
                ('alergias', models.CharField(blank=True, max_length=200, null=True)),
                ('congenital', models.CharField(blank=True, max_length=200, verbose_name='Congenitas')),
                ('general', models.CharField(blank=True, max_length=200)),
                ('nutricional', models.CharField(blank=True, max_length=200)),
                ('otros', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='AntecedenteFamiliar',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='antecedente_familiar', serialize=False, to='persona.Persona')),
                ('sindrome_coronario_agudo', models.BooleanField(default=False, verbose_name='cardiopatia')),
                ('hipertension', models.BooleanField(default=False, verbose_name='Hipertensi\xf3n Arterial')),
                ('tabaquismo', models.BooleanField(default=False)),
                ('epoc', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False, verbose_name='Diabetes Mellitus')),
                ('tuberculosis', models.BooleanField(default=False)),
                ('asma', models.BooleanField(default=False)),
                ('colitis', models.BooleanField(default=False)),
                ('sinusitis', models.BooleanField(default=False)),
                ('colelitiasis', models.BooleanField(default=False)),
                ('migrana', models.BooleanField(default=False)),
                ('obesidad', models.BooleanField(default=False)),
                ('dislipidemias', models.BooleanField(default=False)),
                ('alcoholismo', models.BooleanField(default=False)),
                ('cancer', models.BooleanField(default=False)),
                ('tiroides', models.BooleanField(default=False)),
                ('alergias', models.CharField(blank=True, max_length=200, null=True)),
                ('congenital', models.CharField(blank=True, max_length=200)),
                ('general', models.CharField(blank=True, max_length=200)),
                ('nutricional', models.CharField(blank=True, max_length=200)),
                ('otros', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='AntecedenteObstetrico',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='antecedente_obstetrico', serialize=False, to='persona.Persona')),
                ('menarca', models.DateField(default=datetime.date.today)),
                ('ultimo_periodo', models.DateField(blank=True, null=True)),
                ('gestas', models.IntegerField(default=0)),
                ('partos', models.IntegerField(default=0)),
                ('cesareas', models.IntegerField(default=0)),
                ('otros', models.CharField(blank=True, max_length=200)),
                ('displasia', models.BooleanField(default=False)),
                ('anticoncepcion', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='EstiloVida',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='estilo_vida', serialize=False, to='persona.Persona')),
                ('consume_tabaco', models.BooleanField(default=False)),
                ('inicio_consumo_tabaco', models.CharField(blank=True, max_length=30)),
                ('tipo_de_tabaco', models.CharField(blank=True, max_length=30)),
                ('consumo_diario_tabaco', models.IntegerField(default=0)),
                ('vino', models.BooleanField(default=False)),
                ('cerveza', models.BooleanField(default=False)),
                ('licor', models.BooleanField(default=False)),
                ('cafe', models.BooleanField(default=False)),
                ('cantidad_cafe', models.CharField(blank=True, max_length=200)),
                ('dieta', models.CharField(blank=True, max_length=200)),
                ('cantidad', models.CharField(blank=True, max_length=200)),
                ('numero_comidas', models.IntegerField(null=True)),
                ('tipo_de_comidas', models.CharField(blank=True, max_length=200)),
                ('consume_drogas', models.BooleanField(default=False)),
                ('drogas', models.CharField(blank=True, max_length=200)),
                ('otros', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Fisico',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='persona.Persona')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('lateralidad', models.CharField(blank=True, choices=[(b'D', 'Derecha'), (b'I', 'Izquierda')], max_length=1)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('color_de_ojos', models.CharField(blank=True, max_length=200)),
                ('color_de_cabello', models.CharField(blank=True, max_length=200)),
                ('factor_rh', models.CharField(blank=True, choices=[(b'+', '+'), (b'-', '-')], max_length=1)),
                ('tipo_de_sangre', models.CharField(blank=True, choices=[(b'A', 'A'), (b'B', 'B'), (b'AB', 'AB'), (b'O', 'O')], max_length=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='persona',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Ciudad'),
        ),
        migrations.AddField(
            model_name='historiafisica',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='empleo',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleos', to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='empleo',
            name='sede',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empleos', to='persona.Sede'),
        ),
        migrations.AddField(
            model_name='antecedentequirurgico',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antecedentes_quirurgicos', to='persona.Persona'),
        ),
    ]
