# -*- coding: utf-8 -*-
from django.contrib import admin
from nightingale.models import (SignoVital, Evolucion, Cargo, OrdenMedica,
    Ingesta, Excreta, Glucosuria, Glicemia, Insulina, Sumario, Medicamento,
    FrecuenciaLectura)

admin.site.register(SignoVital)
admin.site.register(Evolucion)
admin.site.register(Cargo)
admin.site.register(OrdenMedica)
admin.site.register(Ingesta)
admin.site.register(Excreta)
admin.site.register(Insulina)
admin.site.register(Glicemia)
admin.site.register(Glucosuria)
admin.site.register(Sumario)
admin.site.register(FrecuenciaLectura)
admin.site.register(Medicamento)

