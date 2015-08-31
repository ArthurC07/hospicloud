# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150528_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='prefijo_recibo',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
