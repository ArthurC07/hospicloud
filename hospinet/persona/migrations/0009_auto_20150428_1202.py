# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0008_auto_20150427_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedente',
            name='tiroides',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='tiroides',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
