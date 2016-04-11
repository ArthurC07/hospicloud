# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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
from django.conf.urls import url

from inventory import views

urlpatterns = [

    url(r'^$',
        views.IndexView.as_view(),
        name='inventario-index'),

    url(r'^itemtemplate/agregar$',
        views.ItemTemplateCreateView.as_view(),
        name='itemtemplate-create'),

    url(r'^itemtemplate/buscar$',
        views.ItemTemplateSearchView.as_view(),
        name='itemtemplate-search'),

    url(r'^itemtemplate/(?P<pk>\d+)$',
        views.ItemTemplateDetailView.as_view(),
        name='itemtemplate'),

    url(r'^itemtemplate/(?P<pk>\d+)/editar$',
        views.ItemTemplateUpdateView.as_view(),
        name='itemtemplate-edit'),

    url(r'^itemtemplate/$',
        views.ItemTemplateListView.as_view(),
        name='itemtemplate-list'),

    url(r'^itemtype/agregar$',
        views.ItemTypeCreateView.as_view(),
        name='itemtype-create'),

    url(r'^itemtype/(?P<pk>\d+)$',
        views.ItemTypeDetailView.as_view(),
        name='item-type'),

    url(r'^itemtype/list$',
        views.ItemTypeListView.as_view(),
        name='itemtype-list'),

    url(r'^inventario/agregar$',
        views.InventarioCreateView.as_view(),
        name='inventario-create'),

    url(r'^inventario/(?P<pk>\d+)$',
        views.InventarioDetailView.as_view(),
        name='inventario'),

    url(r'^(?P<inventario>\d+)/item/agregar$',
        views.ItemCreateView.as_view(),
        name='item-create'),

    url(r'^(?P<inventario>\d+)/item/list$',
        views.ItemInventarioListView.as_view(),
        name='inventario-item-list'),

    url(r'^(?P<inventario>\d+)/requisicion/agregar$',
        views.RequisicionCreateView.as_view(),
        name='requisicion-create'),

    url(r'^requisicion/(?P<pk>\d+)$',
        views.RequisicionDetailView.as_view(),
        name='requisicion'),

    url(r'^requisicion/(?P<pk>\d+)/completar$',
        views.RequisicionUpdateView.as_view(),
        name='requisicion-completar'),

    url(r'^requisicion/(?P<requisicion>\d+)/item/agregar$',
        views.ItemRequisicionCreateView.as_view(),
        name='item-requisicion-create'),

    url(r'^requisicion/(?P<requisicion>\d+)/transferencia/agregar$',
        views.TransferenciaCreateView.as_view(),
        name='transferencia-create'),

    url(r'^transferencia/(?P<pk>\d+)$',
        views.TransferenciaDetailView.as_view(),
        name='transferencia'),

    url(r'^transferencia/(?P<pk>\d+)/efectuar$',
        views.TransferenciaUpdateView.as_view(),
        name='transferencia-efectuar'),

    url(r'^transferencia/(?P<transferencia>\d+)/transferido/agregar$',
        views.TransferidoCreateView.as_view(),
        name='transferido-create'),

    url(r'^(?P<inventario>\d+)/compra/agregar$',
        views.CompraCreateView.as_view(),
        name='compra-create'),

    url(r'^(?P<inventario>\d+)/historial/agregar$',
        views.HistorialCreateView.as_view(),
        name='historial-create'),

    url(r'^compra/(?P<pk>\d+)$',
        views.CompraDetailView.as_view(),
        name='compra'),

    url(r'^compra/(?P<pk>\d+)/edit$',
        views.CompraUpdateView.as_view(),
        name='compra-edit'),

    url(r'^historial/(?P<pk>\d+)$',
        views.HistorialDetailView.as_view(),
        name='historial'),

    url(r'^compra/(?P<compra>\d+)/item/agregar$',
        views.ItemCompradoCreateView.as_view(),
        name='compra-item-create'),

    url(r'^requisicion/item(?P<pk>\d+)/borrar$',
        views.ItemRequisicionDeleteView.as_view(),
        name='itemrequisicion-delete'),

    url(r'^proveedor/(?P<pk>\d+)$',
        views.ProveedorDetailView.as_view(),
        name='proveedor'),

    url(r'^proveedor/(?P<pk>\d+)/editar$',
        views.ProveedorUpdateView.as_view(),
        name='proveedor-edit'),

    url(r'^proveedor/$',
        views.ProveedorListView.as_view(),
        name='proveedor-list'),

    url(r'^proveedor/agregar$',
        views.ProveedorCreateView.as_view(),
        name='proveedor-create'),

    url(r'^cotizacion/agregar$',
        views.CotizacionCreateView.as_view(),
        name='cotizacion-create'),

    url(r'^cotizacion$',
        views.CotizacionListView.as_view(),
        name='cotizacion-list'),

    url(r'^cotizacion/(?P<pk>\d+)$',
        views.CotizacionDetailView.as_view(),
        name='cotizacion-view'),

    url(r'^cotizacion/(?P<cotizacion>\d+)/item/agregar$',
        views.ItemCotizadoCreateView.as_view(),
        name='itemcotizado-create'),
]
