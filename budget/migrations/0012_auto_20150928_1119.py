# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_auto_20150923_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fuente',
            options={'ordering': ('nombre',)},
        ),
    ]
