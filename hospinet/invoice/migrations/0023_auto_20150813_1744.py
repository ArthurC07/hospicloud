# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0022_auto_20150813_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagocuenta',
            old_name='inicial',
            new_name='monto',
        ),
    ]
