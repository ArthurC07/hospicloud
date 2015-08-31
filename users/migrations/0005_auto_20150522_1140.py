# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150522_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='prefijo_recibo',
        ),
        migrations.AddField(
            model_name='ciudad',
            name='prefijo_recibo',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
