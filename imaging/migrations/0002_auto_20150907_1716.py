# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imaging', '0001_squashed_0004_auto_20150831_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='efectuado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='examen',
            name='pendiente',
            field=models.BooleanField(default=True),
        ),
    ]
