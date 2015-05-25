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
                            CierreTurno)


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


admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Venta)
admin.site.register(Pago)
admin.site.register(TipoPago)
admin.site.register(TurnoCaja, TurnoCajaAdmin)
admin.site.register(CierreTurno, CierreturnoAdmin)
