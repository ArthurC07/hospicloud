# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0029_auto_20150528_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aseguradora',
            name='nombre',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
