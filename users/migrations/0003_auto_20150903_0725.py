# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150831_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='correlativo_de_comprobante',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='prefijo_comprobante',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
