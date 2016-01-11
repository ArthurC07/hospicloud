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
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
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
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('contratos', models.IntegerField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
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
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, null=True, blank=True)),
                ('tipo_items', models.ForeignKey(related_name='tipo_eventos', blank=True, to='inventory.ItemType', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
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
        ),
        migrations.AddField(
            model_name='prebeneficiario',
            name='precontrato',
            field=models.ForeignKey(related_name='prebeneficiarios', to='contracts.Precontrato'),
        ),
        migrations.AddField(
            model_name='pago',
            name='tipo_de_pago',
            field=models.ForeignKey(related_name='pagos', to='contracts.TipoPago', null=True),
        ),
        migrations.AddField(
            model_name='limiteevento',
            name='plan',
            field=models.ForeignKey(related_name='limites', to='contracts.Plan'),
        ),
        migrations.AddField(
            model_name='limiteevento',
            name='tipo_evento',
            field=models.ForeignKey(related_name='limites', to='contracts.TipoEvento'),
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(related_name='eventos', to='contracts.TipoEvento'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='plan',
            field=models.ForeignKey(related_name='contratos', to='contracts.Plan'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='vendedor',
            field=models.ForeignKey(related_name='contratos', to='contracts.Vendedor'),
        ),
        migrations.AddField(
            model_name='cancelacion',
            name='contrato',
            field=models.ForeignKey(related_name='cancelaciones', to='contracts.Contrato'),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='contrato',
            field=models.ForeignKey(related_name='beneficiarios', to='contracts.Contrato'),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='persona',
            field=models.ForeignKey(related_name='beneficiarios', to='persona.Persona'),
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='inscripcion',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 19000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cancelacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 24000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='ultimo_pago',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 17000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 23000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 0, 56, 59, 20000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='inscripcion',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 372000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cancelacion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 384000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='ultimo_pago',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 368000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 380000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 7, 14, 52, 25, 375000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='inscripcion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cancelacion',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='ultimo_pago',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='evento',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Aseguradora',
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
        ),
        migrations.CreateModel(
            name='Beneficio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, null=True, blank=True)),
                ('valor', models.DecimalField(default=0, verbose_name=b'precio', max_digits=10, decimal_places=2)),
                ('descuento', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('plan', models.ForeignKey(related_name='beneficios', to='contracts.Plan')),
                ('activo', models.BooleanField(default=True)),
                ('observacion', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='MasterContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicio', models.DateField(default=django.utils.timezone.now)),
                ('vencimiento', models.DateField(default=django.utils.timezone.now)),
                ('aseguradora', models.ForeignKey(related_name='master_contracts', to='contracts.Aseguradora')),
                ('contratante', models.ForeignKey(related_name='master_contracts', blank=True, to='persona.Empleador', null=True)),
                ('plan', models.ForeignKey(related_name='master_contracts', to='contracts.Plan')),
                ('vendedor', models.ForeignKey(related_name='master_contracts', to='contracts.Vendedor')),
                ('processed', models.BooleanField(default=False)),
                ('adicionales', models.IntegerField(default=0)),
                ('comision', models.IntegerField(default=0)),
                ('poliza', models.CharField(max_length=255, null=True, blank=True)),
                ('item', models.ForeignKey(blank=True, to='inventory.ItemTemplate', null=True)),
                ('gastos_medicos', models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)),
                ('vida', models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)),
                ('porcentaje', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterModelOptions(
            name='beneficio',
            options={'ordering': ['nombre']},
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='dependiente',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contrato',
            name='certificado',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='contrato',
            name='poliza',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.RemoveField(
            model_name='plan',
            name='adicionales',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='comision',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='empresarial',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='medicamentos',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='precontrato',
        ),
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('archivo', models.FileField(upload_to=b'contracts/import/%Y/%m/%d')),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='PCD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('numero', models.CharField(unique=True, max_length=255)),
                ('pc', models.IntegerField(default=0)),
                ('persona', models.ForeignKey(related_name='pcds', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='contrato',
            name='titular',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='numero',
            field=models.BigIntegerField(),
        ),
        migrations.AddField(
            model_name='contrato',
            name='master',
            field=models.ForeignKey(related_name='contratos', verbose_name=b'Contrato', blank=True, to='contracts.MasterContract', null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='consulta',
            field=models.ForeignKey(related_name='plan', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.RemoveField(
            model_name='beneficio',
            name='valor',
        ),
        migrations.AddField(
            model_name='beneficio',
            name='descuento_post_limite',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='beneficio',
            name='limite',
            field=models.IntegerField(default=0, verbose_name='L\xedmite de Eventos'),
        ),
        migrations.AddField(
            model_name='beneficio',
            name='tipo_items',
            field=models.ForeignKey(related_name='beneficios', blank=True, to='inventory.ItemType', null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='administradores',
            field=models.ManyToManyField(related_name='contratos', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='beneficio',
            name='aplicar_a_suspendidos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contrato',
            name='suspendido',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='representante',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='nombre',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='nombre',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='aseguradora',
            name='cardex',
            field=models.ForeignKey(related_name='cardex', blank=True, to='persona.Persona', null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='item',
            field=models.ForeignKey(related_name='planes_precio', blank=True, to='inventory.ItemTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='numero',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='exclusion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='exclusion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='vencimiento',
            field=models.DateTimeField(),
        ),
    ]
