# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userprofile_bsc2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='domingo',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='jueves',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='lunes',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='martes',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='miercoles',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='sabado',
        ),
        migrations.RemoveField(
            model_name='turno',
            name='viernes',
        ),
        migrations.AlterField(
            model_name='turno',
            name='fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='turno',
            name='inicio',
            field=models.DateTimeField(),
        ),
    ]
