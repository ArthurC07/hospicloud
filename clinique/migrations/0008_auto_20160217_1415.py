# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 20:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0007_auto_20160215_0804'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='espera',
            options={'ordering': ['created']},
        ),
    ]
