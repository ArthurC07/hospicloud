# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 18:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20160328_1924'),
        ('inventory', '0008_cotizacion_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='ciudad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Ciudad'),
        ),
    ]