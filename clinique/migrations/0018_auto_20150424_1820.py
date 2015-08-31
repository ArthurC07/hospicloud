# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0017_remove_notaenfermeria_consultorio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluacion',
            name='consultorio',
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='usuario',
            field=models.ForeignKey(related_name='evaluaciones', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
