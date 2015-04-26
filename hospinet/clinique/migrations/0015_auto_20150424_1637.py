# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def expand_paciente(apps, schema_editor):
    Consulta = apps.get_model("clinique", "Consulta")

    for consulta in Consulta.objects.all():
        consulta.persona = consulta.paciente.persona
        consulta.consultorio = consulta.paciente.consultorio
        consulta.save()

    Evaluacion = apps.get_model("clinique", "Evaluacion")

    for evaluacion in Evaluacion.objects.all():
        evaluacion.persona = evaluacion.paciente.persona
        evaluacion.consultorio = evaluacion.paciente.consultorio
        evaluacion.save()

    Seguimiento = apps.get_model("clinique", "Seguimiento")

    for seguimiento in Seguimiento.objects.all():
        seguimiento.persona = seguimiento.paciente.persona
        seguimiento.consultorio = seguimiento.paciente.consultorio
        seguimiento.save()

    DiagnosticoClinico = apps.get_model("clinique", "DiagnosticoClinico")

    for diagnostico in DiagnosticoClinico.objects.all():
        diagnostico.persona = diagnostico.paciente.persona
        diagnostico.consultorio = diagnostico.paciente.consultorio
        diagnostico.save()

    OrdenMedica = apps.get_model("clinique", "OrdenMedica")

    for orden in OrdenMedica.objects.all():
        orden.persona = orden.paciente.persona
        orden.consultorio = orden.paciente.consultorio
        orden.save()

    Cargo = apps.get_model("clinique", "Cargo")

    for cargo in Cargo.objects.all():
        cargo.persona = cargo.paciente.persona
        cargo.consultorio = cargo.paciente.consultorio
        cargo.save()

    NotaEnfermeria = apps.get_model("clinique", "NotaEnfermeria")

    for nota in NotaEnfermeria.objects.all():
        nota.persona = nota.paciente.persona
        nota.consultorio = nota.paciente.consultorio
        nota.save()

    Prescripcion = apps.get_model("clinique", "Prescripcion")

    for prescripcion in Prescripcion.objects.all():
        prescripcion.persona = prescripcion.paciente.persona
        prescripcion.consultorio = prescripcion.paciente.consultorio
        prescripcion.save()

    Incapacidad = apps.get_model("clinique", "Incapacidad")

    for incapacidad in Incapacidad.objects.all():
        incapacidad.persona = incapacidad.paciente.persona
        incapacidad.consultorio = incapacidad.paciente.consultorio
        incapacidad.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clinique', '0014_prescripcion_persona'),
    ]

    operations = [
        migrations.RunPython(expand_paciente),
    ]
