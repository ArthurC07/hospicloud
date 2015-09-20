# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultado',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
