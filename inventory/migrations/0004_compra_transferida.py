# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20160428_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='transferida',
            field=models.BooleanField(default=False),
        ),
    ]
