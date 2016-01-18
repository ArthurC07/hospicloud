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
from __future__ import unicode_literals

from django.conf.urls import url

from budget import views

urlpatterns = [

    url(r'^$', views.PresupuestoListView.as_view(), name='budget-index'),

    url(r'^(?P<pk>\d+)$', views.PresupuestoDetailView.as_view(), name='budget'),

    url(r'^mes/list$', views.PresupuestoMesListView.as_view(),
        name='budget-list'),

    url(r'^mes/(?P<pk>\d+)/update$', views.PresupuestoMesUpdateView.as_view(),
        name='monthly-budget-update'),

    url(r'^anual', views.PresupuestoAnualView.as_view(), name='anual-budget'),

    url(r'^(?P<pk>\d+)/control$', views.PresupuestoDetailView.as_view(
            template_name='budget/presupuesto_control.html'),
        name='budget-control'),

    url(r'^mes/(?P<pk>\d+)$', views.PresupuestoMesDetailView.as_view(),
        name='monthly-budget'),

    url(r'^mes/agregar$', views.PresupuestoMesCreateView.as_view(),
        name='monthly-budget-add'),

    url(r'^(?P<presupuesto>\d+)/cuenta/agregar$',
        views.CuentaCreateView.as_view(),
        name='budget-cuenta-agregar'),

    url(r'^cuenta/(?P<cuenta>\d+)/gasto/agregar$',
        views.GastoCreateView.as_view(),
        name='budget-gasto-agregar'),

    url(r'^cuenta/(?P<cuenta>\d+)/gasto/pendiente/agregar$',
        views.GastoPendienteCreateView.as_view(),
        name='budget-gasto-pendiente-agregar'),

    url(r'^gasto/(?P<pk>\d+)$',
        views.GastoDeleteView.as_view(),
        name='gasto-delete'),

    url(r'^gasto/(?P<pk>\d+)/ejecutar$',
        views.GastoEjecutarView.as_view(),
        name='gasto-ejecutar'),

    url(r'^gasto/(?P<pk>\d+)/schedule$',
        views.GastoScheduleView.as_view(),
        name='gasto-schedule'),

    url(r'^gasto/(?P<gasto>\d+)/parcial$',
        views.GastoParcialFormView.as_view(),
        name='gasto-parcial'),

    url(r'^gasto/periodo$',
        views.GastoCuentaPeriodoView.as_view(),
        name='gasto-periodo'),

    url(r'^presupuesto/gasto/periodo$',
        views.GastoPresupuestoPeriodoView.as_view(),
        name='gasto-presupuesto-periodo'),
]
