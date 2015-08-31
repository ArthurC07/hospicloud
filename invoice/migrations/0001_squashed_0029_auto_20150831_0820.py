# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from constance import config

from django.db import models, migrations
import persona.fields
import django_extensions.db.fields
from decimal import Decimal
import django.utils.timezone
from django.conf import settings


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# invoice.migrations.0004_recibo_ciudad
# invoice.migrations.0015_venta_monto
# invoice.migrations.0013_venta_total
# invoice.migrations.0002_recibo_correlativo


def update_correlativo(apps, schema_editor):
    Recibo = apps.get_model("invoice", "Recibo")

    for recibo in Recibo.objects.all():
        recibo.correlativo = config.INVOICE_OFFSET + recibo.id
        recibo.save()


def update_ciudad(apps, schema_editor):
    Recibo = apps.get_model("invoice", "Recibo")

    for recibo in Recibo.objects.exclude(cajero__isnull=True,
                                         cajero__profile__isnull=True):
        recibo.ciudad = recibo.cajero.profile.ciudad
        recibo.save()

def create_total(apps, schema_editor):

    Venta = apps.get_model("invoice", "Venta")

    for venta in Venta.objects.all():
        venta.monto = venta.precio * venta.cantidad
        venta.save()


def create_total(apps, schema_editor):

    Venta = apps.get_model("invoice", "Venta")

    for venta in Venta.objects.all():
        venta.total = venta.tax + venta.precio * venta.cantidad - venta.discount
        venta.save()


class Migration(migrations.Migration):

    replaces = [(b'invoice', '0001_initial'), (b'invoice', '0002_recibo_correlativo'), (b'invoice', '0003_auto_20150522_1155'), (b'invoice', '0004_recibo_ciudad'), (b'invoice', '0005_auto_20150528_1948'), (b'invoice', '0006_recibo_emision'), (b'invoice', '0007_statuspago'), (b'invoice', '0008_pago_status'), (b'invoice', '0009_auto_20150615_1705'), (b'invoice', '0010_auto_20150615_1715'), (b'invoice', '0011_auto_20150615_1715'), (b'invoice', '0012_auto_20150615_1716'), (b'invoice', '0013_venta_total'), (b'invoice', '0014_tipopago_color'), (b'invoice', '0015_venta_monto'), (b'invoice', '0016_auto_20150704_1823'), (b'invoice', '0017_auto_20150707_1815'), (b'invoice', '0018_tipopago_solo_asegurados'), (b'invoice', '0019_statuspago_next_status'), (b'invoice', '0020_cuentaporcobrar'), (b'invoice', '0021_auto_20150810_0712'), (b'invoice', '0022_auto_20150813_1713'), (b'invoice', '0023_auto_20150813_1744'), (b'invoice', '0024_tipopago_reembolso'), (b'invoice', '0024_statuspago_previous_status'), (b'invoice', '0025_merge'), (b'invoice', '0026_notification'), (b'invoice', '0027_auto_20150827_1309'), (b'invoice', '0028_auto_20150828_0929'), (b'invoice', '0029_auto_20150831_0820')]

    dependencies = [
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        ('persona', '0014_persona_ciudad'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
        ('users', '0001_squashed_0011_ciudad_tiene_presupuesto_global'),
    ]

    operations = [
        migrations.CreateModel(
            name='CierreTurno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
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
                ('monto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('comprobante', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('remite', models.CharField(max_length=255, null=True, blank=True)),
                ('radiologo', models.CharField(max_length=255, null=True, blank=True)),
                ('discount', models.DecimalField(default=0, max_digits=7, decimal_places=2)),
                ('cerrado', models.BooleanField(default=False)),
                ('nulo', models.BooleanField(default=False)),
                ('cajero', models.ForeignKey(related_name='recibos', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('cliente', models.ForeignKey(related_name='recibos', to='persona.Persona')),
                ('tipo_de_venta', models.ForeignKey(blank=True, to='inventory.TipoVenta', null=True)),
            ],
            options={
                'permissions': (('cajero', 'Permite al usuario gestionar caja'),),
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
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
            name='TurnoCaja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('inicio', models.DateTimeField(null=True, blank=True)),
                ('fin', models.DateTimeField(null=True, blank=True)),
                ('apertura', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('finalizado', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(related_name='turno_caja', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('precio', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('impuesto', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('descuento', models.IntegerField(default=0)),
                ('placas', models.IntegerField(default=0)),
                ('descontable', models.BooleanField(default=True)),
                ('item', models.ForeignKey(related_name='ventas', blank=True, to='inventory.ItemTemplate', null=True)),
                ('recibo', models.ForeignKey(related_name='ventas', to='invoice.Recibo')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='pago',
            name='recibo',
            field=models.ForeignKey(related_name='pagos', to='invoice.Recibo'),
        ),
        migrations.AddField(
            model_name='pago',
            name='tipo',
            field=models.ForeignKey(related_name='pagos', to='invoice.TipoPago'),
        ),
        migrations.AddField(
            model_name='cierreturno',
            name='pago',
            field=models.ForeignKey(related_name='cierres', to='invoice.TipoPago'),
        ),
        migrations.AddField(
            model_name='cierreturno',
            name='turno',
            field=models.ForeignKey(related_name='cierres', to='invoice.TurnoCaja'),
        ),
        migrations.AddField(
            model_name='recibo',
            name='correlativo',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(
            code=update_correlativo,
        ),
        migrations.AlterField(
            model_name='turnocaja',
            name='apertura',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2),
        ),
        migrations.AddField(
            model_name='recibo',
            name='ciudad',
            field=models.ForeignKey(related_name='recibos', blank=True, to='users.Ciudad', null=True),
        ),
        migrations.RunPython(
            code=update_ciudad,
        ),
        migrations.RemoveField(
            model_name='recibo',
            name='radiologo',
        ),
        migrations.RemoveField(
            model_name='recibo',
            name='remite',
        ),
        migrations.AddField(
            model_name='recibo',
            name='credito',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recibo',
            name='emision',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='StatusPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=255, blank=True)),
                ('reportable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='pago',
            name='status',
            field=models.ForeignKey(related_name='pagos', blank=True, to='invoice.StatusPago', null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='discount',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='tax',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='impuesto',
            field=models.DecimalField(default=0, max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='total',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.RunPython(
            code=create_total,
        ),
        migrations.AddField(
            model_name='tipopago',
            name='color',
            field=persona.fields.ColorField(default=b'', max_length=10),
        ),
        migrations.AddField(
            model_name='venta',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.RunPython(
            code=create_total,
        ),
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='cierreturno',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='tipopago',
            name='solo_asegurados',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statuspago',
            name='next_status',
            field=models.ForeignKey(to='invoice.StatusPago', null=True),
        ),
        migrations.CreateModel(
            name='CuentaPorCobrar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField()),
                ('minimum', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.ForeignKey(to='invoice.StatusPago')),
                ('inicial', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(default=Decimal('0'), max_digits=11, decimal_places=2),
        ),
        migrations.CreateModel(
            name='PagoCuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField()),
                ('cuenta', models.ForeignKey(to='invoice.CuentaPorCobrar')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='tipopago',
            name='reembolso',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statuspago',
            name='previous_status',
            field=models.ForeignKey(related_name='previous', to='invoice.StatusPago', null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('completada', models.BooleanField(default=False)),
                ('recibo', models.ForeignKey(to='invoice.Recibo')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('discount', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('facturada', models.BooleanField(default=False)),
                ('ciudad', models.ForeignKey(blank=True, to='users.Ciudad', null=True)),
                ('persoa', models.ForeignKey(to='persona.Persona')),
                ('tipo_de_venta', models.ForeignKey(to='inventory.TipoVenta')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('cajero', 'Permite al usuario gestionar caja'),),
            },
        ),
        migrations.CreateModel(
            name='Cotizado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.TextField(blank=True)),
                ('porcentaje_descuento', models.IntegerField(default=0)),
                ('precio', models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)),
                ('impuesto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('discount', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('tax', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('total', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('monto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('descontable', models.BooleanField(default=True)),
                ('cotizacion', models.ForeignKey(to='invoice.Cotizacion')),
                ('item', models.ForeignKey(to='inventory.ItemTemplate')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.RemoveField(
            model_name='venta',
            name='placas',
        ),
        migrations.AlterField(
            model_name='venta',
            name='discount',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='impuesto',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='precio',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='tax',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.RenameField(
            model_name='cotizacion',
            old_name='persoa',
            new_name='persona',
        ),
    ]
