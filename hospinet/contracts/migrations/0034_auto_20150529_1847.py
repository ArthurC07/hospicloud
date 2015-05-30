# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0033_plan_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='poliza',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
