# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
import persona.fields
import django_extensions.db.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# persona.migrations.0004_auto_20150427_0843
# persona.migrations.0005_antecedentequirurgico_id
# persona.migrations.0006_auto_20150427_2015
# persona.migrations.0003_auto_20150426_2247


def fix_antecedente(apps, schema_editor):
    Antecedente = apps.get_model("persona", "Antecedente")

    for antecedente in Antecedente.objects.all():

        if antecedente.alcoholismo is None:
            antecedente.alcoholismo = False
        if antecedente.cancer is None:
            antecedente.cancer = False
        if antecedente.colesterol is None:
            antecedente.colesterol = False
        if antecedente.obesidad is None:
            antecedente.obesidad = False
        if antecedente.trigliceridos is None:
            antecedente.trigliceridos = False
        if antecedente.migrana is None:
            antecedente.migrana = False

        antecedente.save()


def fix_another_antecedente(apps, schema_editor):
    Antecedente = apps.get_model("persona", "AntecedenteFamiliar")

    for antecedente in Antecedente.objects.all():

        if antecedente.epoc is None:
            antecedente.epoc = False

        antecedente.save()


def fix_antecedente_again(apps, schema_editor):
    Antecedente = apps.get_model("persona", "AntecedenteQuirurgico")

    for antecedente in Antecedente.objects.all():

        antecedente.id = antecedente.persona.id

        antecedente.save()


def yaaf(apps, schema_editor):
    Antecedente = apps.get_model("persona", "AntecedenteQuirurgico")

    for antecedente in Antecedente.objects.all():

        antecedente.id = antecedente.persona.id

        antecedente.save()

class Migration(migrations.Migration):

    replaces = [(b'persona', '0001_initial'), (b'persona', '0002_auto_20150113_0902'), (b'persona', '0003_auto_20150426_2247'), (b'persona', '0004_auto_20150427_0843'), (b'persona', '0005_antecedentequirurgico_id'), (b'persona', '0006_auto_20150427_2015'), (b'persona', '0007_auto_20150427_2027'), (b'persona', '0008_auto_20150427_2028'), (b'persona', '0009_auto_20150428_1202'), (b'persona', '0010_auto_20150504_1025'), (b'persona', '0011_auto_20150507_1637'), (b'persona', '0012_persona_rtn'), (b'persona', '0013_persona_mostrar_en_cardex')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=200, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('numero_empleado', models.CharField(max_length=200, null=True, blank=True)),
                ('empleador', models.ForeignKey(related_name='empleos', blank=True, to='persona.Empleador', null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_identificacion', models.CharField(blank=True, max_length=1, choices=[(b'T', 'Tarjeta de Identidad'), (b'P', 'Pasaporte'), (b'L', 'Licencia'), (b'N', 'Ninguno')])),
                ('identificacion', models.CharField(max_length=20, blank=True)),
                ('nombre', models.CharField(max_length=50, blank=True)),
                ('apellido', models.CharField(max_length=50, blank=True)),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[(b'M', 'Masculino'), (b'F', 'Femenino')])),
                ('nacimiento', models.DateField(default=datetime.date.today)),
                ('estado_civil', models.CharField(blank=True, max_length=1, choices=[(b'S', 'Soltero/a'), (b'D', 'Divorciado/a'), (b'C', 'Casado/a'), (b'U', 'Union Libre')])),
                ('profesion', models.CharField(max_length=200, blank=True)),
                ('telefono', models.CharField(max_length=200, blank=True)),
                ('celular', models.CharField(max_length=200, blank=True)),
                ('domicilio', models.CharField(max_length=200, blank=True)),
                ('email', models.CharField(max_length=200, blank=True)),
                ('fax', models.CharField(max_length=200, blank=True)),
                ('fotografia', models.ImageField(null=True, upload_to=b'persona/foto//%Y/%m/%d', blank=True)),
                ('nacionalidad', persona.fields.OrderedCountryField(blank=True, max_length=2)),
                ('duplicado', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('persona', 'Permite al usuario gestionar persona'),),
            },
        ),
        migrations.CreateModel(
            name='Fisico',
            fields=[
                ('persona', models.OneToOneField(primary_key=True, serialize=False, to='persona.Persona')),
                ('peso', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('lateralidad', models.CharField(blank=True, max_length=1, choices=[(b'D', 'Derecha'), (b'I', 'Izquierda')])),
                ('altura', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('color_de_ojos', models.CharField(max_length=200, blank=True)),
                ('color_de_cabello', models.CharField(max_length=200, blank=True)),
                ('factor_rh', models.CharField(blank=True, max_length=1, choices=[(b'+', '+'), (b'-', '-')])),
                ('tipo_de_sangre', models.CharField(blank=True, max_length=2, choices=[(b'A', 'A'), (b'B', 'B'), (b'AB', 'AB'), (b'O', 'O')])),
            ],
        ),
        migrations.CreateModel(
            name='EstiloVida',
            fields=[
                ('persona', models.OneToOneField(related_name='estilo_vida', primary_key=True, serialize=False, to='persona.Persona')),
                ('consume_tabaco', models.BooleanField(default=False)),
                ('inicio_consumo_tabaco', models.CharField(max_length=30, blank=True)),
                ('tipo_de_tabaco', models.CharField(max_length=30, blank=True)),
                ('consumo_diario_tabaco', models.IntegerField(null=True)),
                ('vino', models.BooleanField(default=False)),
                ('cerveza', models.BooleanField(default=False)),
                ('licor', models.BooleanField(default=False)),
                ('cafe', models.BooleanField(default=False)),
                ('cantidad_cafe', models.CharField(max_length=200, blank=True)),
                ('dieta', models.CharField(max_length=200, blank=True)),
                ('cantidad', models.CharField(max_length=200, blank=True)),
                ('numero_comidas', models.IntegerField(null=True)),
                ('tipo_de_comidas', models.CharField(max_length=200, blank=True)),
                ('consume_drogas', models.BooleanField(default=False)),
                ('drogas', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AntecedenteQuirurgico',
            fields=[
                ('persona', models.ForeignKey(related_name='antecedentes_quirurgicos', primary_key=True, serialize=False, to='persona.Persona')),
                ('procedimiento', models.CharField(max_length=200, blank=True)),
                ('fecha', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AntecedenteObstetrico',
            fields=[
                ('persona', models.OneToOneField(related_name='antecedente_obstetrico', primary_key=True, serialize=False, to='persona.Persona')),
                ('menarca', models.DateField(default=datetime.date.today)),
                ('ultimo_periodo', models.DateField(null=True, blank=True)),
                ('displasia', models.BooleanField(default=False)),
                ('gestas', models.CharField(max_length=200, blank=True)),
                ('partos', models.CharField(max_length=200, blank=True)),
                ('anticoncepcion', models.CharField(max_length=200, blank=True)),
                ('cesareas', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AntecedenteFamiliar',
            fields=[
                ('persona', models.OneToOneField(related_name='antecedente_familiar', primary_key=True, serialize=False, to='persona.Persona')),
                ('sindrome_coronario_agudo', models.BooleanField(default=False)),
                ('hipertension', models.BooleanField(default=False)),
                ('tabaquismo', models.BooleanField(default=False)),
                ('epoc', models.NullBooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
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
                ('alergias', models.CharField(max_length=200, null=True, blank=True)),
                ('congenital', models.CharField(max_length=200, blank=True)),
                ('general', models.CharField(max_length=200, blank=True)),
                ('nutricional', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('persona', models.OneToOneField(primary_key=True, serialize=False, to='persona.Persona')),
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
                ('migrana', models.NullBooleanField(default=False)),
                ('obesidad', models.NullBooleanField(default=False)),
                ('colesterol', models.NullBooleanField(default=False)),
                ('trigliceridos', models.NullBooleanField(default=False)),
                ('alcoholismo', models.NullBooleanField(default=False)),
                ('cancer', models.NullBooleanField(default=False)),
                ('alergias', models.CharField(max_length=200, null=True, blank=True)),
                ('congenital', models.CharField(max_length=200, blank=True)),
                ('general', models.CharField(max_length=200, blank=True)),
                ('nutricional', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('lugar', models.CharField(max_length=200, blank=True)),
                ('direccion', models.TextField()),
                ('empleador', models.ForeignKey(related_name='sedes', blank=True, to='persona.Empleador', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='empleo',
            name='persona',
            field=models.ForeignKey(related_name='empleos', to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='empleo',
            name='sede',
            field=models.ForeignKey(related_name='empleos', blank=True, to='persona.Sede', null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='fotografia',
            field=models.ImageField(help_text=b'El archivo debe estar en formato jpg o png y no pesar mas de 120kb', null=True, upload_to=b'persona/foto//%Y/%m/%d', blank=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='tipo_identificacion',
            field=models.CharField(blank=True, max_length=1, choices=[(b'R', 'Carnet de Residencia'), (b'L', 'Licencia'), (b'P', 'Pasaporte'), (b'T', 'Tarjeta de Identidad'), (b'N', 'Ninguno')]),
        ),
        migrations.RunPython(
            code=fix_antecedente,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='alcoholismo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='cancer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='colesterol',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='migrana',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='obesidad',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='trigliceridos',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            code=fix_another_antecedente,
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='epoc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='antecedentequirurgico',
            name='id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.RunPython(
            code=fix_antecedente_again,
        ),
        migrations.AlterField(
            model_name='antecedentequirurgico',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.RunPython(
            code=yaaf,
        ),
        migrations.AlterField(
            model_name='antecedentequirurgico',
            name='persona',
            field=models.ForeignKey(related_name='antecedentes_quirurgicos', to='persona.Persona'),
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='anticoncepcion',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='cesareas',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='gestas',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='otros',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='partos',
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='anticoncepcion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='cesareas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='gestas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='otros',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='partos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='antecedente',
            name='tiroides',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='tiroides',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='diabetes',
            field=models.BooleanField(default=False, verbose_name='Diabetes Mellitus'),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='hipertension',
            field=models.BooleanField(default=False, verbose_name='Hipertensi\xf3n Arterial'),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='congenital',
            field=models.CharField(max_length=200, verbose_name='Congenitas', blank=True),
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='migrana',
            field=models.BooleanField(default=False, verbose_name='Migra\xf1a'),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='sindrome_coronario_agudo',
            field=models.BooleanField(default=False, verbose_name='cardiopatia'),
        ),
        migrations.AlterField(
            model_name='estilovida',
            name='consumo_diario_tabaco',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='persona',
            name='rtn',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='mostrar_en_cardex',
            field=models.BooleanField(default=False),
        ),
    ]
