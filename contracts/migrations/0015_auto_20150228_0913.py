# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0014_auto_20150223_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcd',
            name='numero',
            field=models.BigIntegerField(unique=True),
            preserve_default=True,
        ),
    ]
