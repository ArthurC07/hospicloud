# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0030_auto_20150504_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoconsulta',
            name='facturable',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
