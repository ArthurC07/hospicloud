# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0019_auto_20150427_0804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='consulta_horario_extendido',
        ),
    ]
