# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0018_auto_20150424_1820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescripcion',
            name='consulta',
        ),
    ]
