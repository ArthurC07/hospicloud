# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 16:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('clinique', '0025_auto_20160411_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenLaboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('enviado', models.BooleanField(default=False)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinique.Consulta')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='OrdenLaboratorioItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ItemTemplate')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinique.OrdenLaboratorio')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
