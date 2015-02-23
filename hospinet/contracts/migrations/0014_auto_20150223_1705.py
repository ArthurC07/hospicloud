# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0013_auto_20150223_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importfile',
            name='archivo',
            field=models.FileField(upload_to=b'contracts/import/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
