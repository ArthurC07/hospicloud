# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0025_remove_diagnosticoclinico_consultorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='espera',
            name='consulta',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='espera',
            name='fin',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='espera',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='espera',
            name='terminada',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
