# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django_extensions.db.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('imagen', models.FileField(upload_to=b'contracts/autorizaciones/%Y/%m/%d')),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('vigente', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Beneficiario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inscripcion', models.DateTimeField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 301000, tzinfo=utc))),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cancelacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 315000, tzinfo=utc))),
                ('motivo', models.TextField()),
                ('pago', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('numero', models.IntegerField()),
                ('inicio', models.DateField()),
                ('vencimiento', models.DateField()),
                ('ultimo_pago', models.DateTimeField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 297000, tzinfo=utc))),
                ('renovacion', models.DateField(null=True, blank=True)),
                ('cancelado', models.BooleanField(default=False)),
                ('administradores', models.ManyToManyField(related_name='contratos', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('empresa', models.ForeignKey(related_name='contratos', blank=True, to='persona.Empleador', null=True)),
                ('persona', models.ForeignKey(related_name='contratos', to='persona.Persona')),
            ],
            options={
                'permissions': (('contrato', 'Permite al usuario gestionar contratos'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateTimeField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 312000, tzinfo=utc))),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('adjunto', models.FileField(null=True, upload_to=b'evento/%Y/%m/%d', blank=True)),
                ('precio', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('contrato', models.ForeignKey(related_name='eventos', to='contracts.Contrato')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LimiteEvento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 314000, tzinfo=utc))),
                ('contratos', models.IntegerField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255)),
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
                ('fecha', models.DateTimeField(default=datetime.datetime(2014, 12, 26, 21, 33, 19, 304000, tzinfo=utc))),
                ('precio', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('facturar', models.BooleanField(default=False)),
                ('ciclo', models.BooleanField(default=False)),
                ('contrato', models.ForeignKey(related_name='pagos', to='contracts.Contrato')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, null=True, blank=True)),
                ('precio', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('edad_maxima', models.IntegerField()),
                ('adicionales', models.IntegerField()),
                ('medicamentos', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('empresarial', models.BooleanField(default=False)),
                ('comision', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('precontrato', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(related_name='planes', blank=True, to='persona.Empleador', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prebeneficiario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('persona', models.ForeignKey(related_name='prebeneficiarios', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Precontrato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('completado', models.BooleanField(default=False)),
                ('de_acuerdo', models.BooleanField(default=True)),
                ('metodo_de_pago', models.ForeignKey(related_name='precontratos', blank=True, to='contracts.MetodoPago', null=True)),
                ('persona', models.ForeignKey(related_name='precontratos', to='persona.Persona')),
                ('plan', models.ForeignKey(related_name='precontratos', blank=True, to='contracts.Plan', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoEvento',
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
            name='TipoPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('item', models.ForeignKey(related_name='tipos_pago', to='inventory.ItemTemplate')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(related_name='vendedores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prebeneficiario',
            name='precontrato',
            field=models.ForeignKey(related_name='prebeneficiarios', to='contracts.Precontrato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pago',
            name='tipo_de_pago',
            field=models.ForeignKey(related_name='pagos', to='contracts.TipoPago', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='limiteevento',
            name='plan',
            field=models.ForeignKey(related_name='limites', to='contracts.Plan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='limiteevento',
            name='tipo_evento',
            field=models.ForeignKey(related_name='limites', to='contracts.TipoEvento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(related_name='eventos', to='contracts.TipoEvento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrato',
            name='plan',
            field=models.ForeignKey(related_name='contratos', to='contracts.Plan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contrato',
            name='vendedor',
            field=models.ForeignKey(related_name='contratos', to='contracts.Vendedor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cancelacion',
            name='contrato',
            field=models.ForeignKey(related_name='cancelaciones', to='contracts.Contrato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='contrato',
            field=models.ForeignKey(related_name='beneficiarios', to='contracts.Contrato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='persona',
            field=models.ForeignKey(related_name='beneficiarios', to='persona.Persona'),
            preserve_default=True,
        ),
    ]
