# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_squashed_0039_auto_20150817_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastercontract',
            name='ultimo',
            field=models.IntegerField(default=0),
        ),
    ]
