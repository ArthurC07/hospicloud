# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 16:05
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Examen = apps.get_model("clinique", "Examen")
    for examen in Examen.objects.all():
        examen.persona = examen.paciente.persona


class Migration(migrations.Migration):
    dependencies = [
        ('clinique', '0002_examen_persona'),
    ]

    operations = [
        migrations.RunPython(forwards_func, migrations.RunPython.noop)
    ]