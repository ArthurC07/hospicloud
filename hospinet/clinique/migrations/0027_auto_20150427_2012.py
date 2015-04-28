# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0026_auto_20150426_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultorio',
            options={'ordering': ['nombre'], 'permissions': (('consultorio', 'Permite al usuario gestionar consultorios'),)},
        ),
    ]
