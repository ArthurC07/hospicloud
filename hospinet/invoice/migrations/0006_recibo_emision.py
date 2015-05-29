# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20150528_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='emision',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
