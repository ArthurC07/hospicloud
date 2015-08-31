# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20150121_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='vencimiento',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
