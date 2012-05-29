# -*- coding: utf-8 -*-
from django.contrib import admin
from persona.models import (Persona, EstiloVida, Fisico, Antecedente,
    AntecedenteQuirurgico, AntecedenteObstetrico, AntecedenteFamiliar)

admin.site.register(Persona)
admin.site.register(Fisico)
admin.site.register(EstiloVida)
admin.site.register(Antecedente)
admin.site.register(AntecedenteQuirurgico)
admin.site.register(AntecedenteObstetrico)
admin.site.register(AntecedenteFamiliar)
