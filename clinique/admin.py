# -*- coding: utf-8 -*-
from django.contrib import admin
from clinique.models import Esperador, Consultorio, Transaccion, Paciente, Cita

admin.site.register(Consultorio)
admin.site.register(Transaccion)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Esperador)
