# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0038_mastercontract_porcentaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='vencimiento',
            field=models.DateTimeField(),
        ),
    ]
