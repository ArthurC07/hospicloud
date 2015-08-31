# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_ciudad(apps, schema_editor):
    Recibo = apps.get_model("invoice", "Recibo")

    for recibo in Recibo.objects.exclude(cajero__isnull=True,
                                         cajero__profile__isnull=True):
        recibo.ciudad = recibo.cajero.profile.ciudad
        recibo.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_auto_20150522_1140'),
        ('invoice', '0003_auto_20150522_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='ciudad',
            field=models.ForeignKey(related_name='recibos', blank=True,
                                    to='users.Ciudad', null=True),
        ),
        migrations.RunPython(update_ciudad),
    ]
