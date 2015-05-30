# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0034_auto_20150529_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='numero',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
