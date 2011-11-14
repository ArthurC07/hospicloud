# -*- coding: utf-8 -*-
from django.contrib import admin
from nightingale.models import (SignoVital, Evolucion, Cargo, OrdenMedica,
    Ingesta, Excreta, Glucometria, Sumario, FrecuenciaLectura)

admin.site.register(SignoVital)
admin.site.register(Evolucion)
admin.site.register(Cargo)
admin.site.register(OrdenMedica)
admin.site.register(Ingesta)
admin.site.register(Excreta)
admin.site.register(Glucometria)
admin.site.register(Sumario)
admin.site.register(FrecuenciaLectura)
