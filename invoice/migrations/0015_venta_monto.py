# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_total(apps, schema_editor):

    Venta = apps.get_model("invoice", "Venta")

    for venta in Venta.objects.all():
        venta.monto = venta.precio * venta.cantidad
        venta.save()


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0014_tipopago_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='monto',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.RunPython(create_total),
    ]
