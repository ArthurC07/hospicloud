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
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from inventory.models import ItemTemplate, Inventario, Requisicion, ItemType, \
    TipoVenta, Item, ItemComprado, ItemRequisicion, Transferencia, Transferido, \
    Proveedor, Compra, Transaccion, Cotizacion, ItemCotizado


class InventarioAdmin(admin.ModelAdmin):
    list_display = ['lugar', 'ciudad', 'activo', 'puede_comprar']


class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'costo', 'precio_de_venta', 'get_types',
                    'activo', 'servicio']
    list_filter = ('activo',)
    ordering = ('descripcion', 'activo', 'precio_de_venta', 'costo')
    filter_horizontal = ('item_type',)
    search_fields = ['descripcion', ]


class ItemAdmin(admin.ModelAdmin):
    list_display = ('plantilla', 'inventario', 'vencimiento', 'cantidad')
    ordering = ['plantilla__descripcion', 'inventario', 'vencimiento',
                'created']
    search_fields = ['plantilla__descripcion', 'inventario__lugar']


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rtn', 'telefono']
    search_fields = ['name', 'rtn']
    ordering = ['name', 'rtn']


class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['item', 'cantidad', 'user']


class CotizacionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['proveedor', 'created', 'vencimiento', 'autorizada',
                    'comprada', 'denegada']
    ordering = ['proveedor__name', 'created', 'vencimiento', 'autorizada',
                'comprada', 'denegada']
    search_fields = ['proveedor__name']


class ItemCotizadoAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['get_proveedor', 'item', 'created', 'cantidad',
                    'precio']
    ordering = ['cotizacion__proveedor__name', 'item__descripcion', 'created',
                'cantidad', 'precio']
    search_fields = ['cotizacion__proveedor__name', 'item__descripcion']

    def get_proveedor(self, obj):
        return obj.cotizacion.proveedor.name


admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Requisicion)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(ItemType)
admin.site.register(TipoVenta)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transferido)
admin.site.register(Transferencia)
admin.site.register(Compra)
admin.site.register(ItemComprado)
admin.site.register(ItemRequisicion)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Transaccion, TransaccionAdmin)
admin.site.register(Cotizacion, CotizacionAdmin)
admin.site.register(ItemCotizado, ItemCotizadoAdmin)
