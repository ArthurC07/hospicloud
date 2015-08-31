# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150223_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='prefijo_recibo',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
