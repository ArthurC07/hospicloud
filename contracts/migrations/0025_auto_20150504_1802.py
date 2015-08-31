# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0024_tipoevento_tipo_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficio',
            name='limite',
            field=models.IntegerField(default=0, verbose_name='L\xedmite de Eventos'),
            preserve_default=True,
        ),
    ]
