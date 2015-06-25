# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0038_auto_20150623_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='remitida',
            field=models.BooleanField(default=False),
        ),
    ]
