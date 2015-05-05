# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_item_vencimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='consulta',
            field=models.BooleanField(default=True, verbose_name=b'Aparece en Cargos de Consulta'),
            preserve_default=True,
        ),
    ]
