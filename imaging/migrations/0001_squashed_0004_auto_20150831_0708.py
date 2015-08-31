# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    replaces = [(b'imaging', '0001_initial'), (b'imaging', '0002_auto_20150829_1917'), (b'imaging', '0003_auto_20150831_0705'), (b'imaging', '0004_auto_20150831_0708')]

    dependencies = [
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.FileField(upload_to=b'examen/adjunto/%Y/%m/%d')),
                ('descripcion', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dicom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('archivo', models.FileField(upload_to=b'examen/dicom/%Y/%m/%d')),
                ('descripcion', models.CharField(max_length=255, blank=True)),
                ('convertido', models.BooleanField(default=False)),
                ('imagen', models.ImageField(upload_to=b'examen/dicom/imagen/%Y/%m/%d', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estudio',
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
            name='EstudioProgramado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('remitio', models.CharField(max_length=200)),
                ('efectuado', models.NullBooleanField(default=False)),
                ('persona', models.ForeignKey(related_name='estudios_progamados', to='persona.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now)),
                ('remitio', models.CharField(max_length=200, null=True)),
                ('facturado', models.NullBooleanField(default=False)),
                ('persona', models.ForeignKey(related_name='examenes', to='persona.Persona')),
            ],
            options={
                'permissions': (('examen', 'Permite al usuario gestionar examenes'),),
            },
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'examen/imagen/%Y/%m/%d')),
                ('descripcion', models.CharField(max_length=255, blank=True)),
                ('examen', models.ForeignKey(related_name='imagenes', to='imaging.Examen')),
            ],
        ),
        migrations.CreateModel(
            name='Radiologo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, blank=True)),
                ('porcentaje', models.IntegerField(default=30)),
                ('item', models.ForeignKey(blank=True, to='inventory.ItemTemplate', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, blank=True)),
                ('porcentaje', models.IntegerField(default=10)),
                ('item', models.ForeignKey(blank=True, to='inventory.ItemTemplate', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='TipoExamen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('item', models.ForeignKey(blank=True, to='inventory.ItemTemplate', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='examen',
            name='radiologo',
            field=models.ForeignKey(related_name='examenes', to='imaging.Radiologo'),
        ),
        migrations.AddField(
            model_name='examen',
            name='tecnico',
            field=models.ForeignKey(related_name='examenes', blank=True, to='imaging.Tecnico', null=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='tipo_de_examen',
            field=models.ForeignKey(related_name='examenes', to='imaging.TipoExamen'),
        ),
        migrations.AddField(
            model_name='examen',
            name='tipo_de_venta',
            field=models.ForeignKey(related_name='examenes', to='inventory.TipoVenta'),
        ),
        migrations.AddField(
            model_name='examen',
            name='usuario',
            field=models.ForeignKey(related_name='estudios_realizados', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='radiologo',
            field=models.ForeignKey(related_name='estudios', to='imaging.Radiologo'),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='tecnico',
            field=models.ForeignKey(related_name='estudios', blank=True, to='imaging.Tecnico', null=True),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='tipo_de_examen',
            field=models.ForeignKey(related_name='estudios_progamados', to='imaging.TipoExamen'),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='tipo_de_venta',
            field=models.ForeignKey(related_name='estudios', to='inventory.TipoVenta'),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='usuario',
            field=models.ForeignKey(related_name='estudios_programados', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='estudio',
            name='examen',
            field=models.ForeignKey(related_name='estudios', to='imaging.Examen'),
        ),
        migrations.AddField(
            model_name='estudio',
            name='tipo_de_examen',
            field=models.ForeignKey(related_name='estudios', to='imaging.TipoExamen'),
        ),
        migrations.AddField(
            model_name='dicom',
            name='examen',
            field=models.ForeignKey(related_name='dicoms', to='imaging.Examen'),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='examen',
            field=models.ForeignKey(related_name='adjuntos', to='imaging.Examen'),
        ),
        migrations.AlterModelOptions(
            name='dicom',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='estudioprogramado',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='imagen',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='tipoexamen',
            options={'ordering': ('-modified', '-created'), 'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='dicom',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='dicom',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='estudioprogramado',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='examen',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='imagen',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='imagen',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='tipoexamen',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='tipoexamen',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='estudioprogramado',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='examen',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='examen',
            name='facturado',
            field=models.BooleanField(default=False),
        ),
    ]
