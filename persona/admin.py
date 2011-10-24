# -*- coding: utf-8 -*-
from django.contrib import admin
from persona.models import Persona, EstiloVida, Fisico

admin.site.register(Persona)
admin.site.register(Fisico)
admin.site.register(EstiloVida)
