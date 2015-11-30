# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0008_solucion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meta',
            options={'ordering': ('tipo_meta',)},
        ),
    ]
