#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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

from contracts.models import (TipoEvento, Plan, Contrato, Evento, Pago, PCD,
                              Beneficiario, Vendedor, LimiteEvento, TipoPago,
                              Meta, Autorizacion, Precontrato, MetodoPago,
                              Beneficio, Aseguradora, MasterContract,
                              ImportFile)


class BeneficioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'plan', 'activo')
    ordering = ['plan', 'nombre', 'activo']


class PCDAdmin(admin.ModelAdmin):
    list_display = ('numero', 'persona')
    ordering = ['numero', 'persona']
    search_fields = ['persona__nombre', 'persona__apellidos',
                     'numero']


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'persona', 'plan', 'master', 'vencimiento', 'activo')
    ordering = ['numero', 'persona', 'plan', 'master', 'vencimiento']
    search_fields = ['persona__nombre', 'persona__apellidos',
                     'numero']


admin.site.register(Plan)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(TipoEvento)
admin.site.register(Evento)
admin.site.register(LimiteEvento)
admin.site.register(Pago)
admin.site.register(Vendedor)
admin.site.register(Beneficiario)
admin.site.register(TipoPago)
admin.site.register(Meta)
admin.site.register(Autorizacion)
admin.site.register(Precontrato)
admin.site.register(MetodoPago)
admin.site.register(Aseguradora)
admin.site.register(MasterContract)
admin.site.register(PCD, PCDAdmin)
admin.site.register(Beneficio, BeneficioAdmin)
admin.site.register(ImportFile)
