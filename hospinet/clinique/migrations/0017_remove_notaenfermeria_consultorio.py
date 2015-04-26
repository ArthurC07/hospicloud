# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0016_auto_20150424_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notaenfermeria',
            name='consultorio',
        ),
    ]
