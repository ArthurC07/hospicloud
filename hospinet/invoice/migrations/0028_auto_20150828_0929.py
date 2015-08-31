# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0027_auto_20150827_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cotizacion',
            old_name='persoa',
            new_name='persona',
        ),
    ]
