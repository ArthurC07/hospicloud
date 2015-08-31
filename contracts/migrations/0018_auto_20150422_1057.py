# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_contrato_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='master',
            field=models.ForeignKey(related_name='contratos', verbose_name=b'Contrato', blank=True, to='contracts.MasterContract', null=True),
            preserve_default=True,
        ),
    ]
