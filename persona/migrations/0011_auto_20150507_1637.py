# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0010_auto_20150504_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedente',
            name='congenital',
            field=models.CharField(max_length=200, verbose_name='Congenitas', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='migrana',
            field=models.BooleanField(default=False, verbose_name='Migra\xf1a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='sindrome_coronario_agudo',
            field=models.BooleanField(default=False, verbose_name='cardiopatia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='estilovida',
            name='consumo_diario_tabaco',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
