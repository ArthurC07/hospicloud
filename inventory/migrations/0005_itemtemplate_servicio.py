# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_compra_transferida'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtemplate',
            name='servicio',
            field=models.BooleanField(default=False),
        ),
    ]