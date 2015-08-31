# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0018_tipopago_solo_asegurados'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuspago',
            name='next_status',
            field=models.ForeignKey(to='invoice.StatusPago', null=True),
        ),
    ]
