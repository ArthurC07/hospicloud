# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20141227_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='fecha',
            field=models.DateField(default=datetime.date(2015, 1, 7)),
            preserve_default=True,
        ),
    ]
