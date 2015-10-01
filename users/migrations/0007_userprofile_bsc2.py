# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0005_auto_20150930_1814'),
        ('users', '0006_turno'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bsc2',
            field=models.ForeignKey(related_name='usuarios2', blank=True, to='bsc.ScoreCard', null=True),
        ),
    ]
