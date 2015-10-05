# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20151005_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='fin',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='turno',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
