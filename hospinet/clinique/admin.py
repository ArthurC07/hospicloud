# -*- coding: utf-8 -*-
from django.contrib import admin
from clinique.models import (Consultorio, Paciente, Transaccion, Cita,
    Esperador, Consulta, Receta, HistoriaClinica, Optometria)

admin.site.register(Consultorio)
admin.site.register(Paciente)
admin.site.register(Transaccion)
admin.site.register(Cita)
admin.site.register(Esperador)
admin.site.register(Consulta)
admin.site.register(Receta)
admin.site.register(HistoriaClinica)
admin.site.register(Optometria)
