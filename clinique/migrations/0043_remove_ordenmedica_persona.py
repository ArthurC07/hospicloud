# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0042_auto_20150703_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenmedica',
            name='persona',
        ),
    ]
