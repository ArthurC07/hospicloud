# -*- coding: utf-8 -*-
#
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

from django.contrib import admin

from clinique.models import (Paciente, Cita, Consulta, TipoConsulta,
                             Consultorio, Evaluacion, Seguimiento,
                             LecturaSignos,
                             TipoCargo, Cargo, OrdenMedica, Localidad,
                             Especialidad, Espera, Afeccion, Incapacidad)


class IncapacidadAdmin(admin.ModelAdmin):
    list_display = ('persona', 'usuario', 'descripcion', 'created', 'dias')
    ordering = ['persona', 'usuario', 'descripcion', 'created', 'dias']
    search_fields = ['persona__nombre', 'persona__apellido']


class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('persona', 'consultorio', 'created')
    ordering = ['persona', 'consultorio', 'created']
    search_fields = ['persona__nombre', 'persona__apellido',
                     'consultorio__nombre', ]


class ConsultorioAdmin(admin.ModelAdmin):
    filter_horizontal = ('administradores',)
    list_display = ('nombre', 'activo')


admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Incapacidad, IncapacidadAdmin)
admin.site.register(TipoConsulta)
admin.site.register(Consultorio, ConsultorioAdmin)
admin.site.register(Seguimiento)
admin.site.register(Evaluacion)
admin.site.register(LecturaSignos)
admin.site.register(OrdenMedica)
admin.site.register(Cargo)
admin.site.register(TipoCargo)
admin.site.register(Localidad)
admin.site.register(Especialidad)
admin.site.register(Espera)
admin.site.register(Afeccion)
