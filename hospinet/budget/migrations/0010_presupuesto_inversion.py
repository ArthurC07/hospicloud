# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_auto_20150731_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='inversion',
            field=models.BooleanField(default=False),
        ),
    ]
