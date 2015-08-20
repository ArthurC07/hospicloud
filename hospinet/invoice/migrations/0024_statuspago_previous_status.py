# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0023_auto_20150813_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuspago',
            name='previous_status',
            field=models.ForeignKey(related_name='previous', to='invoice.StatusPago', null=True),
        ),
    ]
