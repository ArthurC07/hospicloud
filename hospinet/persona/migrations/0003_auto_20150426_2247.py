# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedente',
            name='alcoholismo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='cancer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='colesterol',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='migrana',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='obesidad',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='trigliceridos',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
