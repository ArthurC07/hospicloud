# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def expand_paciente(apps, schema_editor):
    Incapacidad = apps.get_model("clinique", "Incapacidad")

    for incapacidad in Incapacidad.objects.all():

        incapacidad.usuario = incapacidad.consultorio.usuario
        incapacidad.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0020_incapacidad_usuario'),
    ]

    operations = [
        migrations.RunPython(expand_paciente),
    ]
