# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20150729_1025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0011_ciudad_tiene_presupuesto_global'),
        ('persona', '0014_persona_ciudad'),
        ('invoice', '0026_notification'),
    ]

    operations = [
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
                ('precio', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
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
    ]
