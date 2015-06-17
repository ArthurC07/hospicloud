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

from invoice.models import (Recibo, Venta, Pago, TipoPago, TurnoCaja,
                            CierreTurno, StatusPago)


class ReciboAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero', 'cajero', 'created')
    ordering = ['cliente', 'cajero', 'created']
    search_fields = ['cliente__nombre']


class CierreturnoAdmin(admin.ModelAdmin):
    list_display = ('turno', 'pago', 'monto')
    ordering = ['turno', 'pago', 'monto']
    search_fields = ['turno__usuario__first_name', 'turno__usuario__last_name',
                     'pago__nombre', 'monto']


class TurnoCajaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'inicio', 'fin', 'apertura')
    ordering = ['usuario', 'inicio', 'fin', 'apertura']
    search_fields = ['usuario__first_name', 'usuario__last_name',
                     'pago__nombre', 'apertura']


class TipoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color',)
    ordering = ['nombre', 'color',]


class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'tipo', 'get_recibo_number', 'recibo', 'get_recibo_cajero', 'monto',
        'created', 'status')
    ordering = ['tipo', 'recibo', 'monto', 'created', 'status']
    search_fields = ['recibo__usuario__first_name',
                     'recibo__usuario__last_name',
                     'tipo__nombre', 'monto']

    def get_recibo_number(self, instance):
        ciudad = instance.recibo.ciudad
        if ciudad is None:
            if instance.recibo.cajero is None or \
                            instance.recibo.cajero.profile is None or \
                            instance.recibo.cajero.profile.ciudad is None:
                return instance.recibo.correlativo

            ciudad = instance.recibo.cajero.profile.ciudad

        return u'{0}-{1:08d}'.format(ciudad.prefijo_recibo,
                                     instance.recibo.correlativo)

    def get_recibo_cajero(self, instance):

        return instance.recibo.cajero


admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Venta)
admin.site.register(StatusPago)
admin.site.register(Pago, PagoAdmin)
admin.site.register(TipoPago, TipoPagoAdmin)
admin.site.register(TurnoCaja, TurnoCajaAdmin)
admin.site.register(CierreTurno, CierreturnoAdmin)
