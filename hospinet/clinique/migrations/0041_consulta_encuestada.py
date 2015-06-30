# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0040_auto_20150629_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='encuestada',
            field=models.BooleanField(default=False),
        ),
    ]
