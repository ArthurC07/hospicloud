# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-09 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_company_incapacidad_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='terminado',
            field=models.BooleanField(default=False),
        ),
    ]
