# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_squashed_0029_auto_20150831_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='descripcion',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
