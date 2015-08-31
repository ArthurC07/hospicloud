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
            name='Cobro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField(default=1)),
                ('facturado', models.NullBooleanField(default=False)),
                ('cargo', models.ForeignKey(related_name='cobros', to='inventory.ItemTemplate')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Diagnostico',
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
            name='Emergencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('historia_enfermedad_actual', models.TextField(null=True, blank=True)),
                ('frecuencia_respiratoria', models.IntegerField(null=True, blank=True)),
                ('temperatura', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('presion', models.CharField(max_length=100, null=True, blank=True)),
                ('frecuencia_cardiaca', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('saturacion_de_oxigeno', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('facturada', models.NullBooleanField(default=False)),
                ('persona', models.ForeignKey(related_name='emergencias', to='persona.Persona')),
                ('tipo_de_venta', models.ForeignKey(blank=True, to='inventory.TipoVenta', null=True)),
                ('usuario', models.ForeignKey(related_name='emergencias', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'permissions': (('emergencia', 'Permite al usuario gestionar emergencia'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamenFisico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('orl', models.TextField()),
                ('cardiopulmonar', models.TextField()),
                ('gastrointestinal', models.TextField()),
                ('extremidades', models.TextField()),
                ('otras', models.TextField()),
                ('emergencia', models.ForeignKey(related_name='examenes_fisicos', to='emergency.Emergencia')),
                ('usuario', models.ForeignKey(related_name='examenes_fisicos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hallazgo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('hallazgo', models.TextField()),
                ('emergencia', models.ForeignKey(related_name='hallazgos', to='emergency.Emergencia')),
                ('usuario', models.ForeignKey(related_name='hallazgos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemisionExterna',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('destino', models.CharField(max_length=100)),
                ('diagnostico', models.TextField()),
                ('notas', models.TextField()),
                ('emergencia', models.ForeignKey(related_name='remisiones_externas', to='emergency.Emergencia')),
                ('usuario', models.ForeignKey(related_name='er_rexternas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemisionInterna',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('doctor', models.CharField(max_length=100)),
                ('emergencia', models.ForeignKey(related_name='remisiones_internas', to='emergency.Emergencia')),
                ('usuario', models.ForeignKey(related_name='er_rinternas', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('indicaciones', models.TextField()),
                ('emergencia', models.ForeignKey(related_name='tratamientos', to='emergency.Emergencia')),
                ('usuario', models.ForeignKey(related_name='er_tratamientos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='emergencia',
            field=models.ForeignKey(related_name='diagnosticos', to='emergency.Emergencia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='usuario',
            field=models.ForeignKey(related_name='er_diagnosticos', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cobro',
            name='emergencia',
            field=models.ForeignKey(related_name='cobros', to='emergency.Emergencia'),
            preserve_default=True,
        ),
    ]
