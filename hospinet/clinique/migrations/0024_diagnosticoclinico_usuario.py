# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def extract_user(apps, schema_editor):

    DiagnosticoClinico = apps.get_model("clinique", "DiagnosticoClinico")

    for diagnostico in DiagnosticoClinico.objects.all():
        diagnostico.usuario = diagnostico.consultorio.usuario
        diagnostico.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0023_prescripcion_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosticoclinico',
            name='usuario',
            field=models.ForeignKey(related_name='diagnosticos_clinicos', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(extract_user),
    ]
