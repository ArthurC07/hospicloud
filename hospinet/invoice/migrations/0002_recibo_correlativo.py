# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from constance import config

from django.db import models, migrations


def update_correlativo(apps, schema_editor):
    Recibo = apps.get_model("invoice", "Recibo")

    for recibo in Recibo.objects.all():
        recibo.correlativo = config.INVOICE_OFFSET + recibo.id
        recibo.save()


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='correlativo',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(update_correlativo),
    ]
