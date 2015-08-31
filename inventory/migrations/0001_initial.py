# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('ingresada', models.BooleanField(default=False)),
                ('proveedor', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('fecha', models.DateField(default=datetime.date(2014, 12, 26))),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lugar', models.CharField(default=b'Bodega', max_length=255)),
                ('puede_comprar', models.NullBooleanField(default=False)),
            ],
            options={
                'permissions': (('inventario', 'Permite al usuario gestionar inventario'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('inventario', models.ForeignKey(related_name='items', to='inventory.Inventario')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('action', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemComprado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('ingresado', models.BooleanField(default=False)),
                ('cantidad', models.IntegerField(default=0)),
                ('compra', models.ForeignKey(related_name='items', to='inventory.Compra')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemHistorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('historial', models.ForeignKey(related_name='items', to='inventory.Historial')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemRequisicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField()),
                ('entregada', models.BooleanField(default=False)),
                ('pendiente', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.CharField(max_length=255)),
                ('marca', models.CharField(max_length=32, null=True, blank=True)),
                ('modelo', models.CharField(max_length=32, null=True, blank=True)),
                ('notas', models.TextField(null=True, blank=True)),
                ('precio_de_venta', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('costo', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('unidad_de_medida', models.CharField(max_length=32, null=True, blank=True)),
                ('impuestos', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('activo', models.BooleanField(default=True)),
                ('comision', models.DecimalField(default=Decimal('30.00'), max_digits=4, decimal_places=2)),
                ('comision2', models.DecimalField(default=Decimal('10.00'), max_digits=4, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemType',
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
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='descripci\xf3n')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Requisicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('aprobada', models.NullBooleanField(default=False)),
                ('entregada', models.NullBooleanField(default=False)),
                ('inventario', models.ForeignKey(related_name='requisiciones', blank=True, to='inventory.Inventario', null=True)),
                ('usuario', models.ForeignKey(related_name='requisiciones', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoVenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.CharField(max_length=255, null=True, blank=True)),
                ('incremento', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('disminucion', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('aplicada', models.NullBooleanField(default=False)),
                ('destino', models.ForeignKey(related_name='entradas', blank=True, to='inventory.Inventario', null=True)),
                ('origen', models.ForeignKey(related_name='salidas', blank=True, to='inventory.Inventario', null=True)),
                ('requisicion', models.ForeignKey(related_name='transferencias', blank=True, to='inventory.Requisicion', null=True)),
                ('usuario', models.ForeignKey(related_name='transferencias', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transferido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('cantidad', models.IntegerField()),
                ('aplicada', models.BooleanField(default=False)),
                ('item', models.ForeignKey(related_name='transferidos', to='inventory.ItemTemplate')),
                ('transferencia', models.ForeignKey(related_name='transferidos', to='inventory.Transferencia')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='item_type',
            field=models.ManyToManyField(related_name='items', null=True, to='inventory.ItemType', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemtemplate',
            name='suppliers',
            field=models.ManyToManyField(related_name='plantillas', null=True, to='inventory.Proveedor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemrequisicion',
            name='item',
            field=models.ForeignKey(related_name='requisiciones', to='inventory.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemrequisicion',
            name='requisicion',
            field=models.ForeignKey(related_name='items', to='inventory.Requisicion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemhistorial',
            name='item',
            field=models.ForeignKey(related_name='historicos', to='inventory.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemcomprado',
            name='item',
            field=models.ForeignKey(related_name='comprado', blank=True, to='inventory.ItemTemplate', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemaction',
            name='item',
            field=models.ForeignKey(related_name='acciones', to='inventory.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemaction',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='plantilla',
            field=models.ForeignKey(related_name='items', to='inventory.ItemTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historial',
            name='inventario',
            field=models.ForeignKey(related_name='historiales', to='inventory.Inventario'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='compra',
            name='inventario',
            field=models.ForeignKey(related_name='compras', blank=True, to='inventory.Inventario', null=True),
            preserve_default=True,
        ),
    ]
