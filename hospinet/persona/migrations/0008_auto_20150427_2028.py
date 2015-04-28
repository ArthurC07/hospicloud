# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0007_auto_20150427_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='anticoncepcion',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='cesareas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='gestas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='otros',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='antecedenteobstetrico',
            name='partos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
