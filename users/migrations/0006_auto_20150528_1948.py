# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150522_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='inicio_rango',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='limite_de_emision',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='prefijo_recibo',
            field=models.CharField(default=b'', max_length=100, blank=True),
        ),
    ]
