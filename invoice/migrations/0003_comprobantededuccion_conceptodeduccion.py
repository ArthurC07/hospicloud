# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_squashed_0019_auto_20150729_1025'),
        ('users', '0003_auto_20150903_0725'),
        ('persona', '0014_persona_ciudad'),
        ('invoice', '0002_auto_20150902_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprobanteDeduccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('correlativo', models.IntegerField()),
                ('ciudad', models.ForeignKey(to='users.Ciudad')),
                ('persona', models.ForeignKey(to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='ConceptoDeduccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('monto', models.DecimalField(default=0, max_digits=11, decimal_places=2)),
                ('comprobante', models.ForeignKey(to='invoice.ComprobanteDeduccion')),
                ('concepto', models.ForeignKey(to='inventory.ItemTemplate')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
