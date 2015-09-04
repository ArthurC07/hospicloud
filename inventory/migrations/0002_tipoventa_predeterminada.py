# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoventa',
            name='predeterminada',
            field=models.BooleanField(default=False),
        ),
    ]
