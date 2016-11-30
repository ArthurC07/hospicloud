# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-10 17:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0029_auto_20161101_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='call_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]