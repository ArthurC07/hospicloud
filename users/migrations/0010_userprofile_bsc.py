# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0001_initial'),
        ('users', '0009_ciudad_fin_rango'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bsc',
            field=models.ForeignKey(related_name='usuarios', blank=True, to='bsc.ScoreCard', null=True),
        ),
    ]
