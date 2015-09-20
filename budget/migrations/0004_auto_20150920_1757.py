# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gasto',
            old_name='fuente',
            new_name='fuente_de_pago',
        ),
        migrations.RenameField(
            model_name='gasto',
            old_name='factura',
            new_name='numero_de_factura',
        ),
        migrations.RenameField(
            model_name='gasto',
            old_name='comprobante_entregado',
            new_name='recepcion_de_facturas_originales',
        ),
        migrations.AlterField(
            model_name='concepto',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='concepto',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='presupuestomensual',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='presupuestomensual',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='rubro',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='rubro',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
