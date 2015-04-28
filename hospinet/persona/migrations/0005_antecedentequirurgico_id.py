# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_antecedente(apps, schema_editor):
    Antecedente = apps.get_model("persona", "AntecedenteQuirurgico")

    for antecedente in Antecedente.objects.all():

        antecedente.id = antecedente.persona.id

        antecedente.save()


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0004_auto_20150427_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedentequirurgico',
            name='id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(fix_antecedente)
    ]
