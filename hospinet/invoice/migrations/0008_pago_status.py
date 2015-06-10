# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_statuspago'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='status',
            field=models.ForeignKey(related_name='pagos', blank=True, to='invoice.StatusPago', null=True),
        ),
    ]
