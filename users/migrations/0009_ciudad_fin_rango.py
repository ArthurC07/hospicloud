# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150528_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='fin_rango',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
