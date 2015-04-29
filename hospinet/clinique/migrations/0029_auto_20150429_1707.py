# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def extract_user(apps, schema_editor):

    OrdenMedica = apps.get_model("clinique", "OrdenMedica")

    for orden in OrdenMedica.objects.all():
        orden.usuario = orden.consultorio.usuario
        orden.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clinique', '0028_auto_20150428_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenmedica',
            name='usuario',
            field=models.ForeignKey(related_name='ordenes_clinicas', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(extract_user),
        migrations.RemoveField(
            model_name='ordenmedica',
            name='consultorio',
        ),
    ]
