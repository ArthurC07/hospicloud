# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 19:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20160513_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnomaliaTransferencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('cantidad', models.IntegerField(default=0)),
                ('detalle', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Transferido')),
                ('transferencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Transferencia')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
