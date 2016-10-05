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
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from clinique.models import Cita, Consulta, TipoConsulta, Consultorio, \
    Evaluacion, Seguimiento, LecturaSignos, TipoCargo, Cargo, OrdenMedica, \
    Localidad, Especialidad, Espera, Afeccion, Incapacidad
from contracts.models import MasterContract, Contrato


class IncapacidadAdmin(admin.ModelAdmin):
    list_display = ('persona', 'usuario', 'descripcion', 'created', 'dias')
    ordering = ['persona', 'usuario', 'descripcion', 'created', 'dias']
    search_fields = ['persona__nombre', 'persona__apellido']


class EsperaAdmin(admin.ModelAdmin):
    list_display = (
        'persona', 'consultorio', 'created', 'fecha', 'inicio', 'fin')
    ordering = ['created', 'fecha', 'inicio', 'fin', 'persona',
                'consultorio__usuario']
    search_fields = ['persona__nombre', 'persona__apellido']


class ConsultaAdminForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'

    espera = forms.ModelChoiceField(queryset=Espera.objects.select_related(
        'persona',
        'consultorio',
    ))
    poliza = forms.ModelChoiceField(
        queryset=MasterContract.objects.select_related(
            'aseguradora',
            'plan',
            'contratante',
        ))
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.select_related(
        'persona',
    ))


class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'persona', 'consultorio', 'created', 'contrato',
        'facturada', 'activa', 'remitida',
    )
    ordering = ['persona', 'consultorio', 'created', 'facturada', 'activa',
                'remitida', ]
    search_fields = ['persona__nombre', 'persona__apellido',
                     'consultorio__nombre', ]
    form = ConsultaAdminForm


class ConsultorioAdmin(admin.ModelAdmin):
    filter_horizontal = ('administradores',)
    list_display = ('nombre', 'activo')


class AfeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'habilitado',)
    ordering = ['nombre', 'codigo', 'habilitado', ]
    search_fields = ['nombre', 'codigo']


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
admin.site.register(Espera, EsperaAdmin)
admin.site.register(Afeccion, AfeccionAdmin)
