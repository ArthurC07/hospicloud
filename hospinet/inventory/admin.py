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

from django.contrib import admin
from inventory.models import (ItemTemplate, Inventario, Requisicion, ItemType,
                              TipoVenta, Item, ItemComprado, ItemRequisicion,
                              Transferencia, Transferido, Proveedor, Compra)


class ItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'costo', 'precio_de_venta', 'get_types', 'activo',)
    list_filter = ('activo', )
    ordering = ('descripcion', 'activo', 'precio_de_venta', 'costo')
    filter_horizontal = ('item_type',)
    search_fields = ['descripcion',]


class ItemAdmin(admin.ModelAdmin):
    list_display = ('plantilla', 'inventario', 'vencimiento', 'created')
    ordering = ['plantilla__descripcion', 'inventario', 'vencimiento', 'created']
    search_fields = ['plantilla__descripcion', 'inventario__lugar']


admin.site.register(ItemTemplate, ItemTemplateAdmin)
admin.site.register(Requisicion)
admin.site.register(Inventario)
admin.site.register(ItemType)
admin.site.register(TipoVenta)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transferido)
admin.site.register(Transferencia)
admin.site.register(Compra)
admin.site.register(ItemComprado)
admin.site.register(ItemRequisicion)
admin.site.register(Proveedor)
