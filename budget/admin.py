# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Carlos Flores <cafg10@gmail.com>
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

from budget.models import Presupuesto, Cuenta, Gasto, Income, \
    PresupuestoMensual, Rubro, Concepto


class PresupuestoAdmin(admin.ModelAdmin):
    list_display = (
        'ciudad', 'porcentaje_global', 'inversion', 'activo', 'created')
    ordering = ('ciudad', 'porcentaje_global', 'inversion', 'activo', 'created')
    search_fields = ['ciudad', ]


class CuentaAdmin(admin.ModelAdmin):
    list_display = ['get_ciudad', 'presupuesto', 'nombre', 'limite']
    ordering = ['presupuesto', 'nombre', 'limite']

    def get_ciudad(self, obj):
        return obj.presupuesto.ciudad

    get_ciudad.short_description = 'Ciudad'
    get_ciudad.admin_order_field = 'presupuesto__ciudad'


class GastoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'proveedor', 'cuenta', 'get_presupuesto',
                    'monto', 'ejecutado', 'fecha_de_pago',
                    'fecha_maxima_de_pago']
    ordering = ['descripcion', 'monto']

    def get_ciudad(self, obj):
        return obj.cuenta.presupuesto.ciudad

    def get_presupuesto(self, obj):
        return obj.cuenta.presupuesto

    get_ciudad.short_description = 'Ciudad'
    get_ciudad.admin_order_field = 'cuenta__presupuesto__ciudad'

    get_presupuesto.short_description = 'Presupuesto'
    get_presupuesto.admin_order_field = 'cuenta__presupuesto'


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('ciudad', 'monto', 'activo', 'created')
    ordering = ('ciudad', 'monto', 'activo', 'created')
    search_fields = ['ciudad', ]


class PresupuestoMensualAdmin(admin.ModelAdmin):
    list_display = ['ciudad', 'mes', 'anio']
    ordering = ('ciudad', 'mes', 'anio')


class RubroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_mes', 'get_anio', 'get_ciudad']
    ordering = ('nombre',)

    def get_mes(self, obj):
        return obj.presupuesto.mes

    def get_anio(self, obj):
        return obj.presupuesto.anio

    def get_ciudad(self, obj):
        return obj.presupuesto.ciudad


class ConceptoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'get_rubro', 'get_mes', 'get_anio',
                    'get_ciudad']
    ordering = ('descripcion',)

    def get_mes(self, obj):
        return obj.rubro.presupuesto.mes

    def get_anio(self, obj):
        return obj.rubro.presupuesto.anio

    def get_ciudad(self, obj):
        return obj.rubro.presupuesto.ciudad

    def get_rubro(self, obj):
        return obj.rubro.nombre


admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Gasto, GastoAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(PresupuestoMensual, PresupuestoMensualAdmin)
admin.site.register(Rubro, RubroAdmin)
admin.site.register(Concepto, ConceptoAdmin)
