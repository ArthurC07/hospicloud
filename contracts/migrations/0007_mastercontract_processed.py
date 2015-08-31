# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0006_mastercontract'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastercontract',
            name='processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
