# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0010_auto_20150415_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturasignos',
            name='presion_diastolica',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecturasignos',
            name='presion_sistolica',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecturasignos',
            name='respiracion',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
