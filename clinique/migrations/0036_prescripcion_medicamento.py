# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20150507_1637'),
        ('clinique', '0035_auto_20150507_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescripcion',
            name='medicamento',
            field=models.ForeignKey(related_name='prescripciones', blank=True, to='inventory.ItemTemplate', null=True),
            preserve_default=True,
        ),
    ]
