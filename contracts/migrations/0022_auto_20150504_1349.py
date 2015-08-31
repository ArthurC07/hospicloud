# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0021_beneficio_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficio',
            name='valor',
        ),
        migrations.AddField(
            model_name='beneficio',
            name='descuento_post_limite',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficio',
            name='limite',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
