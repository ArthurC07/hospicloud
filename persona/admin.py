# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

from django.contrib import admin

from persona.models import Persona, EstiloVida, Fisico, Antecedente, \
    AntecedenteQuirurgico, AntecedenteObstetrico, AntecedenteFamiliar, \
    Empleador, Empleo, Sede, HistoriaFisica


class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'id', 'identificacion')
    ordering = ['id', 'nombre', 'apellido', 'identificacion']
    search_fields = ['nombre', 'apellido', 'identificacion']


class HistoriaFisicaAdmin(admin.ModelAdmin):
    list_display = ['persona', 'fecha', 'altura', 'peso']


class EmpleadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion']
    search_fields = ['nombre']
    ordering = ['nombre']


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Fisico)
admin.site.register(EstiloVida)
admin.site.register(Antecedente)
admin.site.register(AntecedenteQuirurgico)
admin.site.register(AntecedenteObstetrico)
admin.site.register(AntecedenteFamiliar)
admin.site.register(Empleador, EmpleadorAdmin)
admin.site.register(Empleo)
admin.site.register(Sede)
admin.site.register(HistoriaFisica, HistoriaFisicaAdmin)
