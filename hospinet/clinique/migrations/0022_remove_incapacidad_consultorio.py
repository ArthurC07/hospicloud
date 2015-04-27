# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0021_auto_20150426_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incapacidad',
            name='consultorio',
        ),
    ]
