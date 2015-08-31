# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0028_auto_20150828_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizado',
            name='precio',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True),
        ),
    ]
