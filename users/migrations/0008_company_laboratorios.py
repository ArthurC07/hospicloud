# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160511_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='laboratorios',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
