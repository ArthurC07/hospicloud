# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0035_auto_20150529_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='exclusion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='exclusion',
            field=models.TextField(blank=True),
        ),
    ]
