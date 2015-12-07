# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_auto_20150920_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='credito',
            field=models.BooleanField(default=False),
        ),
    ]
