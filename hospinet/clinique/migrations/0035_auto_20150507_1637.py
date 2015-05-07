# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0034_auto_20150506_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultorio',
            name='administradores',
            field=models.ManyToManyField(related_name='consultorios_administrados', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
