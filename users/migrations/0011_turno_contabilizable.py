# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20151016_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='contabilizable',
            field=models.BooleanField(default=False),
        ),
    ]
