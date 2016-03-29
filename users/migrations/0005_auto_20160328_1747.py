# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 23:47
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Ciudad = apps.get_model("users", "Ciudad")
    LegalData = apps.get_model("users", "LegalData")
    for ciudad in Ciudad.objects.all():
        ciudad.recibo = LegalData()
        ciudad.recibo.correlativo = ciudad.correlativo_de_recibo
        ciudad.recibo.cai = ciudad.cai_recibo
        ciudad.recibo.prefijo = ciudad.prefijo_recibo
        ciudad.recibo.limite_de_emision = ciudad.limite_de_emision
        ciudad.recibo.inicio = ciudad.inicio_rango
        ciudad.recibo.fin = ciudad.fin_rango
        ciudad.recibo.save()

        ciudad.comprobante = LegalData()
        ciudad.comprobante.correlativo = ciudad.correlativo_de_comprobante
        ciudad.comprobante.cai = ciudad.cai_comprobante
        ciudad.comprobante.prefijo = ciudad.prefijo_comprobante
        ciudad.comprobante.limite_de_emision = ciudad.limite_de_emision_comprobante
        ciudad.comprobante.inicio = ciudad.inicio_rango_comprobante
        ciudad.comprobante.fin = ciudad.fin_rango_comprobante
        ciudad.comprobante.save()

        ciudad.nota_credito = LegalData()
        ciudad.nota_credito.correlativo = ciudad.correlativo_de_nota_de_credito
        ciudad.nota_credito.cai = ciudad.cai_nota_credito
        ciudad.nota_credito.prefijo = ciudad.prefijo_nota_credito
        ciudad.nota_credito.limite_de_emision = ciudad.limite_de_emision_nota_credito
        ciudad.nota_credito.inicio = ciudad.inicio_rango_nota_credito
        ciudad.nota_credito.fin = ciudad.fin_rango_nota_credito
        ciudad.nota_credito.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160328_1723'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop)
    ]
