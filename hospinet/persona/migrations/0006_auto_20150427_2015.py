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
        ('persona', '0005_antecedentequirurgico_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedentequirurgico',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
            preserve_default=True,
        ),
        migrations.RunPython(fix_antecedente),
        migrations.AlterField(
            model_name='antecedentequirurgico',
            name='persona',
            field=models.ForeignKey(related_name='antecedentes_quirurgicos', to='persona.Persona'),
            preserve_default=True,
        ),
    ]
