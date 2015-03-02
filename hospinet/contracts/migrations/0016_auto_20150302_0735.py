# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0015_auto_20150228_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='numero',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
    ]
