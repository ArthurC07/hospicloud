# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0017_auto_20150707_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipopago',
            name='solo_asegurados',
            field=models.BooleanField(default=False),
        ),
    ]
