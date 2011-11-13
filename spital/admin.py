# -*- coding: utf-8 -*-
from django.contrib import admin
from spital.models import (Admision, SignoVital, Evolucion, Cargo, OrdenMedica,
    Ingesta, Excreta, FrecuenciaLectura, Sumario, Glucometria)

admin.site.register(Admision)
admin.site.register(SignoVital)
admin.site.register(Evolucion)
admin.site.register(Cargo)
admin.site.register(OrdenMedica)
admin.site.register(Ingesta)
admin.site.register(Excreta)
admin.site.register(Glucometria)
admin.site.register(Sumario)
admin.site.register(FrecuenciaLectura)
