# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0012_persona_rtn'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='mostrar_en_cardex',
            field=models.BooleanField(default=False),
        ),
    ]
