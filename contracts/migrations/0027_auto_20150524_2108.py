# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0026_auto_20150507_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastercontract',
            name='poliza',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pcd',
            name='numero',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
