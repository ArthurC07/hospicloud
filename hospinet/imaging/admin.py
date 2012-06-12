# -*- coding: utf-8 -*-
from django.contrib import admin
from imaging.models import Examen, Imagen, Adjunto, Dicom, EstudioProgramado

admin.site.register(Examen)
admin.site.register(Imagen)
admin.site.register(Adjunto)
admin.site.register(Dicom)
admin.site.register(EstudioProgramado)
