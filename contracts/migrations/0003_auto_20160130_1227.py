# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_auto_20160128_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='certificado',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]