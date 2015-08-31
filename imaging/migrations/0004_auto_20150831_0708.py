# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imaging', '0003_auto_20150831_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='facturado',
            field=models.BooleanField(default=False),
        ),
    ]
