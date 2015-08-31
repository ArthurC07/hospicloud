# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0022_remove_incapacidad_consultorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='usuario',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
