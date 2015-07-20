# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from budget.views import PresupuestoDetailView, CuentaCreateView, \
    GastoCreateView, PresupuestoListView

urlpatterns = patterns('',

                       url(r'^$',
                           PresupuestoListView.as_view(),
                           name='budget-index'),

                       url(r'^(?P<pk>\d+)$',
                           PresupuestoDetailView.as_view(),
                           name='budget'),

                       url(r'^(?P<presupuesto>\d+)/cuenta/agregar$',
                           CuentaCreateView.as_view(),
                           name='budget-cuenta-agregar'),

                       url(r'^cuenta/(?P<cuenta>\d+)/gasto/agregar$',
                           GastoCreateView.as_view(),
                           name='budget-gasto-agregar'),

                       )
