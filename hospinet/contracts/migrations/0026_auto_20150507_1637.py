# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0025_auto_20150504_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='administradores',
            field=models.ManyToManyField(related_name='contratos', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
