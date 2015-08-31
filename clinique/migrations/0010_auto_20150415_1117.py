# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
        ('clinique', '0009_auto_20150408_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('motivo', models.TextField()),
                ('consultorio', models.ForeignKey(related_name='remisiones', to='clinique.Consultorio')),
                ('especialidad', models.ForeignKey(related_name='remisiones', blank=True, to='clinique.Especialidad', null=True)),
                ('persona', models.ForeignKey(related_name='remisiones', to='persona.Persona')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoRemision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='remision',
            name='tipo',
            field=models.ForeignKey(related_name='remisiones', to='clinique.TipoRemision'),
            preserve_default=True,
        ),
    ]
