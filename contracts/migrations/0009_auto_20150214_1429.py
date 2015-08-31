# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0008_auto_20150214_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficio',
            options={'ordering': ['nombre']},
        ),
    ]
