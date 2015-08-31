# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bsc', '0005_auto_20150630_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='opcion',
            field=models.ForeignKey(blank=True, to='bsc.Opcion', null=True),
        ),
    ]
