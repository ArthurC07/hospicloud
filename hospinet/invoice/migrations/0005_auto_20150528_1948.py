# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_recibo_ciudad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='radiologo',
        ),
        migrations.RemoveField(
            model_name='recibo',
            name='remite',
        ),
        migrations.AddField(
            model_name='recibo',
            name='credito',
            field=models.BooleanField(default=False),
        ),
    ]
