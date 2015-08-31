# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0037_auto_20150715_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='mastercontract',
            name='porcentaje',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True),
        ),
    ]
