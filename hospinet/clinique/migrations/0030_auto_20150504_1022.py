# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0029_auto_20150429_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Afeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('habilitado', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='afeccion',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to='clinique.Afeccion', null=True),
            preserve_default=True,
        ),
    ]
