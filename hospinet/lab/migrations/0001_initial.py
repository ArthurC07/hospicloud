# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('descripcion', models.TextField()),
                ('archivo', models.FileField(upload_to=b'lab/results/%Y/%m/%d')),
                ('persona', models.ForeignKey(related_name='resultados', to='persona.Persona')),
            ],
            options={
                'permissions': (('lab', 'Permite al usuario administrar laboratorios'),),
            },
            bases=(models.Model,),
        ),
    ]
