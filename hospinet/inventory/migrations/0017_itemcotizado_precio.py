# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_itemcotizado_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcotizado',
            name='precio',
            field=models.DecimalField(default=0, max_digits=11, decimal_places=2),
        ),
    ]
