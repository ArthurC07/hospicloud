# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0006_auto_20150630_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pregunta',
            name='valor',
        ),
    ]
