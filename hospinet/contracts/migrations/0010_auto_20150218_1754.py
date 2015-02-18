# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0009_auto_20150214_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mastercontract',
            name='archivo',
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='adicionales',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='comision',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mastercontract',
            name='poliza',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
