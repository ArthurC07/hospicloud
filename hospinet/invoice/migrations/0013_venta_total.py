# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_total(apps, schema_editor):

    Venta = apps.get_model("invoice", "Venta")

    for venta in Venta.objects.all():
        venta.total = venta.tax + venta.precio * venta.cantidad - venta.discount
        venta.save()


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20150615_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='total',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True),
        ),
        migrations.RunPython(create_total),
    ]
