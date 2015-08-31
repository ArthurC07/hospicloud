# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20150722_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='comprobante',
            field=models.FileField(null=True, upload_to=b'budget/gasto/%Y/%m/%d', blank=True),
        ),
    ]
