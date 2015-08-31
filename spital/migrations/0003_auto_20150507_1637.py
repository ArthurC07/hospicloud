# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spital', '0002_delete_especialidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admision',
            name='fiadores',
            field=models.ManyToManyField(related_name='fianzas', to='persona.Persona', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='admision',
            name='referencias',
            field=models.ManyToManyField(related_name='referencias', to='persona.Persona', blank=True),
            preserve_default=True,
        ),
    ]
