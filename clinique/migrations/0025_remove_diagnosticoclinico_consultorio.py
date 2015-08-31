# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0024_diagnosticoclinico_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosticoclinico',
            name='consultorio',
        ),
    ]
