# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150528_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='direccion',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='telefono',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
