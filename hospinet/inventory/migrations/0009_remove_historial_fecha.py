# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150507_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial',
            name='fecha',
        ),
    ]
