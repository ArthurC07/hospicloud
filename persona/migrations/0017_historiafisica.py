# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0016_auto_20151118_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaFisica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('peso', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('altura', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('persona', models.ForeignKey(to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
