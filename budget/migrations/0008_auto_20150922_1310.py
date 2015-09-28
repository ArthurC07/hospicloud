# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0007_gasto_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasto',
            name='cuenta',
            field=models.ForeignKey(verbose_name='Tipo de Cargo', to='budget.Cuenta'),
        ),
    ]
