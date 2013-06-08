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

from django.conf.urls import patterns, url
from inventory.views import (IndexView, ItemTemplateCreateView,
    ItemTemplateDetailView, ItemTypeCreateView, InventarioCreateView,
    InventarioDetailView)

urlpatterns = patterns('',
    
    url(r'^$',
        IndexView.as_view(),
        name='inventario-index'),
    
    url(r'^itemtemplate/agregar$',
        ItemTemplateCreateView.as_view(),
        name='itemtemplate-create'),
    
    url(r'^itemtemplate/(?P<pk>\d+)$',
        ItemTemplateDetailView.as_view(),
        name='itemtemplate'),
    
    url(r'^itemtype/agregar$',
        ItemTypeCreateView.as_view(),
        name='itemtype-create'),
    
    url(r'^inventario/agregar$',
        InventarioCreateView.as_view(),
        name='inventario-create'),
    
    url(r'^inventario/(?P<pk>\d+)$',
        InventarioDetailView.as_view(),
        name='inventario'),
    
)
