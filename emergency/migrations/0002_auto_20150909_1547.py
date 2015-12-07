# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencia',
            name='facturada',
            field=models.BooleanField(default=False),
        ),
    ]
