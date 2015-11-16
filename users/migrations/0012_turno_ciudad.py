# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_turno_contabilizable'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='ciudad',
            field=models.ForeignKey(blank=True, to='users.Ciudad', null=True),
        ),
    ]
