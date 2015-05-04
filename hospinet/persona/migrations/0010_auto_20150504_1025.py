# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0009_auto_20150428_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='diabetes',
            field=models.BooleanField(default=False, verbose_name='Diabetes Mellitus'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='hipertension',
            field=models.BooleanField(default=False, verbose_name='Hipertensi\xf3n Arterial'),
            preserve_default=True,
        ),
    ]
