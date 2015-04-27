# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0019_remove_prescripcion_consulta'),
    ]

    operations = [
        migrations.AddField(
            model_name='incapacidad',
            name='usuario',
            field=models.ForeignKey(related_name='incapacidades', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
