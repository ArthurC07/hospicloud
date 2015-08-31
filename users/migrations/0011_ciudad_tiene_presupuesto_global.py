# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_userprofile_bsc'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='tiene_presupuesto_global',
            field=models.BooleanField(default=False),
        ),
    ]
