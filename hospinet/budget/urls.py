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
    GastoCreateView, PresupuestoListView, GastoDeleteView, \
    GastoPendienteCreateView, GastoEjecutarView

urlpatterns = patterns('',

                       url(r'^$',
                           PresupuestoListView.as_view(),
                           name='budget-index'),

                       url(r'^(?P<pk>\d+)$',
                           PresupuestoDetailView.as_view(),
                           name='budget'),

                       url(r'^(?P<pk>\d+)/control$',
                           PresupuestoDetailView.as_view(
                               template_name='budget/presupuesto_control.html'),
                           name='budget-control'),

                       url(r'^(?P<presupuesto>\d+)/cuenta/agregar$',
                           CuentaCreateView.as_view(),
                           name='budget-cuenta-agregar'),

                       url(r'^cuenta/(?P<cuenta>\d+)/gasto/agregar$',
                           GastoCreateView.as_view(),
                           name='budget-gasto-agregar'),

                       url(r'^cuenta/(?P<cuenta>\d+)/gasto/pendiente/agregar$',
                           GastoPendienteCreateView.as_view(),
                           name='budget-gasto-pendiente-agregar'),

                       url(r'^gasto/(?P<pk>\d+)$',
                           GastoDeleteView.as_view(),
                           name='gasto-delete'),

                       url(r'^gasto/(?P<pk>\d+)/ejecutar$',
                           GastoEjecutarView.as_view(),
                           name='gasto-ejecutar'),
                       )
