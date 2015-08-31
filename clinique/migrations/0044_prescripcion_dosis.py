# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0043_remove_ordenmedica_persona'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='dosis',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
