# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0011_auto_20150219_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='adicionales',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='comision',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='empresarial',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='medicamentos',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='precontrato',
        ),
    ]
