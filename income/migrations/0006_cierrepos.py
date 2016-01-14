# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0005_auto_20160106_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='CierrePOS',
            fields=[
                ('deposito_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='income.Deposito')),
                ('batch', models.CharField(max_length=255)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='income.Banco')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=('income.deposito',),
        ),
    ]