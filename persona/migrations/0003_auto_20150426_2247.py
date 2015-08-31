# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_antecedente(apps, schema_editor):
    Antecedente = apps.get_model("persona", "Antecedente")

    for antecedente in Antecedente.objects.all():

        if antecedente.alcoholismo is None:
            antecedente.alcoholismo = False
        if antecedente.cancer is None:
            antecedente.cancer = False
        if antecedente.colesterol is None:
            antecedente.colesterol = False
        if antecedente.obesidad is None:
            antecedente.obesidad = False
        if antecedente.trigliceridos is None:
            antecedente.trigliceridos = False
        if antecedente.migrana is None:
            antecedente.migrana = False
            
        antecedente.save()


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20150113_0902'),
    ]

    operations = [
        migrations.RunPython(fix_antecedente),
        migrations.AlterField(
            model_name='antecedente',
            name='alcoholismo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='cancer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='colesterol',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='migrana',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='obesidad',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='antecedente',
            name='trigliceridos',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
