# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='fecha',
            field=models.DateField(default=datetime.date(2014, 12, 27)),
            preserve_default=True,
        ),
    ]
