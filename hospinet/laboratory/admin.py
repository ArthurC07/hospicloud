# -*- coding: utf-8 -*-
from django.contrib import admin
from laboratory.models import Examen, Imagen, Adjunto, Dicom

admin.site.register(Examen)
admin.site.register(Imagen)
admin.site.register(Adjunto)
admin.site.register(Dicom)
