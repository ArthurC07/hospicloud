# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0006_auto_20150427_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='anticoncepcion',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='cesareas',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='gestas',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='otros',
        ),
        migrations.RemoveField(
            model_name='antecedenteobstetrico',
            name='partos',
        ),
    ]
