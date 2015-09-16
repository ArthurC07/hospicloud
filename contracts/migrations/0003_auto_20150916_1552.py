# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_mastercontract_ultimo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mastercontract',
            old_name='ultimo',
            new_name='ultimo_certificado',
        ),
    ]
