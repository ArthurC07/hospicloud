# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0009_auto_20150703_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='voto',
            name='sugerencia',
            field=models.TextField(null=True, blank=True),
        ),
    ]
