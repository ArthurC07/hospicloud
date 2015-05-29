# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0031_aseguradora_cardex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aseguradora',
            name='rtn',
        ),
        migrations.AlterField(
            model_name='aseguradora',
            name='representante',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
