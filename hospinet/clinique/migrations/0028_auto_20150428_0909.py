# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0027_auto_20150427_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='consultorio',
        ),
        migrations.RemoveField(
            model_name='cargo',
            name='persona',
        ),
        migrations.AddField(
            model_name='cargo',
            name='consulta',
            field=models.ForeignKey(related_name='cargos', blank=True, to='clinique.Consulta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cargo',
            name='usuario',
            field=models.ForeignKey(related_name='cargos_clinicos', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
