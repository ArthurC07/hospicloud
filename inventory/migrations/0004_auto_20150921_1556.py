# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150920_1729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proveedor',
            options={'ordering': ('name', 'rtn')},
        ),
    ]
