# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 17:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0007_auto_20160503_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cotizacion_inventario_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
