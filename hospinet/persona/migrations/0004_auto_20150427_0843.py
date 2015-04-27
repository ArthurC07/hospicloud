# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_antecedente(apps, schema_editor):
    Antecedente = apps.get_model("persona", "AntecedenteFamiliar")

    for antecedente in Antecedente.objects.all():

        if antecedente.epoc is None:
            antecedente.epoc = False

        antecedente.save()

class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_auto_20150426_2247'),
    ]

    operations = [
        migrations.RunPython(fix_antecedente),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='epoc',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
