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
from django.contrib import admin

from invoice.models import Recibo, Venta, Pago, TipoPago, TurnoCaja, \
    CierreTurno, StatusPago, CuentaPorCobrar, Cotizacion, DetalleCredito, \
    ComprobanteDeduccion, ConceptoDeduccion, NotaCredito


class ReciboAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero', 'cajero', 'created', 'cerrado', 'nulo')
    ordering = ['cliente', 'cajero', 'created', 'cerrado', 'nulo']
    search_fields = ['cliente__nombre', 'correlativo']


class CierreturnoAdmin(admin.ModelAdmin):
    list_display = ('turno', 'pago', 'monto', 'created')
    ordering = ['turno', 'pago', 'monto', 'created']
    search_fields = ['turno__usuario__first_name', 'turno__usuario__last_name',
                     'monto']


class TurnoCajaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'inicio', 'fin', 'apertura')
    ordering = ['usuario', 'inicio', 'fin', 'apertura']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'apertura']


class TipoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'reembolso')
    ordering = ['nombre', 'color', 'reembolso']


class PagoAdmin(admin.ModelAdmin):
    list_display = (
        'tipo', 'get_recibo_number', 'recibo', 'get_recibo_cajero', 'monto',
        'created', 'status')
    ordering = ['tipo', 'recibo', 'monto', 'created', 'status']
    search_fields = ['recibo__cajero__first_name',
                     'recibo__cajero__last_name',
                     'tipo__nombre', 'monto', 'recibo__correlativo']

    def get_recibo_number(self, instance):
        ciudad = instance.recibo.ciudad
        if ciudad is None:
            if instance.recibo.cajero is None or \
                            instance.recibo.cajero.profile is None or \
                            instance.recibo.cajero.profile.ciudad is None:
                return instance.recibo.correlativo

            ciudad = instance.recibo.cajero.profile.ciudad

        return '{0}-{1:08d}'.format(ciudad.prefijo_recibo,
                                     instance.recibo.correlativo)

    def get_recibo_cajero(self, instance):

        return instance.recibo.cajero


class CuentaPorCobrarAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'created', 'modified', 'minimum', 'status')


class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'recibo', 'item', 'cantidad', 'precio', 'monto', 'total', 'created'
    )
    search_fields = [
        'recibo__id',
        'recibo__numero',
        'recibo__usuario__first_name',
        'recibo__usuario__last_name'
    ]
    ordering = ['created', 'recibo', 'monto']


class StatusPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'reportable', 'pending', 'next_status',
                    'previous_status',)


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'usuario', 'created', 'facturada')
    ordering = ['persona', 'usuario', 'created', 'facturada']
    search_fields = ['persona__nombre', 'persona__apellido']


class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'ciudad', 'correlativo', 'created')
    ordering = ['proveedor', 'ciudad', 'correlativo', 'created']


class ConceptoDeduccionAdmin(admin.ModelAdmin):
    """
    Enables management of :class:`ConceptoDeduccion` instances
    """
    list_display = (
        'comprobante',
        'concepto',
        'get_correlativo',
        'monto',
        'created'
    )
    ordering = [
        'comprobante',
        'concepto',
        'monto',
        'created',
    ]
    search_fields = [
        'comprobante__correlativo',
        'comprobante__persona__nombre',
        'comprobante__persona__apellido',
    ]

    def get_correlativo(self, instance):

        return instance.comprobante.correlativo


class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ['recibo', 'correlativo', 'created']
    search_fields = ['recibo__persona__nombre', 'recibo__persona__apellido',
                     'recibo__correlativo', 'correlativo']


class DetalleCreditoAdmin(admin.ModelAdmin):
    list_display = ['nota', 'item', 'cantidad']


admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(StatusPago, StatusPagoAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(TipoPago, TipoPagoAdmin)
admin.site.register(TurnoCaja, TurnoCajaAdmin)
admin.site.register(CierreTurno, CierreturnoAdmin)
admin.site.register(CuentaPorCobrar, CuentaPorCobrarAdmin)
admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(ComprobanteDeduccion, ComprobanteAdmin)
admin.site.register(ConceptoDeduccion, ConceptoDeduccionAdmin)
admin.site.register(NotaCredito, NotaCreditoAdmin)
admin.site.register(DetalleCredito, DetalleCreditoAdmin)
