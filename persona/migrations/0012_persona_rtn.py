# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0011_auto_20150507_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='rtn',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
