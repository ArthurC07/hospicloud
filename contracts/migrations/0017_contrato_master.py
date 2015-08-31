# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0016_auto_20150302_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='master',
            field=models.ForeignKey(related_name='contratos', blank=True, to='contracts.MasterContract', null=True),
            preserve_default=True,
        ),
    ]
