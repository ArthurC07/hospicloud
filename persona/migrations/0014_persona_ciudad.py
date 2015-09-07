# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0011_ciudad_tiene_presupuesto_global'),
        ('persona', '0001_squashed_0013_persona_mostrar_en_cardex'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='ciudad',
            field=models.ForeignKey(blank=True, to='users.Ciudad', null=True),
        ),
    ]
