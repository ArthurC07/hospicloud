# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 20:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0004_auto_20160106_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cierrepos',
            name='banco',
        ),
        migrations.DeleteModel(
            name='CierrePOS',
        ),
    ]