# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0008_pregunta_calificable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pregunta',
            options={'ordering': ['created']},
        ),
    ]
