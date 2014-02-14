# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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

from contracts.views import (ContratoDetailView, PagoCreateView,
                             EventoDeleteView, PagoDeleteView, EventoCreateView,
                             ContratoUpdateView, IndexView, ContratoCreateView,
                             VendedorSearchView, VendedorDetailView)


urlpatterns = patterns('',

                       url(r'^$',
                           IndexView.as_view(),
                           name='contrato-index'),

                       url(r'^contrato/(?P<pk>\d+)$',
                           ContratoDetailView.as_view(),
                           name='contrato'),

                       url(
                           r'^(?P<persona>\d+)/contrato/agregar$',
                           ContratoCreateView.as_view(),
                           name='contrato-add'),

                       url(r'^contrato/(?P<pk>\d+)/edit$',
                           ContratoUpdateView.as_view(),
                           name='contrato-edit'),

                       url(r'^contrato/(?P<pk>\d+)/pago/add$',
                           PagoCreateView.as_view(),
                           name='contrato-pago-add'),

                       url(r'^contrato/(?P<pk>\d+)/evento/add$',
                           EventoCreateView.as_view(),
                           name='contrato-evento-add'),

                       url(r'^pago/(?P<pk>\d+)/delete$',
                           PagoDeleteView.as_view(),
                           name='contrato-pago-delete'),

                       url(r'^evento/(?P<pk>\d+)/delete$',
                           EventoDeleteView.as_view(),
                           name='contrato'),

                       url(r'^vendedor/buscar$',
                           VendedorSearchView.as_view(),
                           name='vendedor-search'),

                       url(r'^vendedor/(?P<pk>\d+)$',
                           VendedorDetailView.as_view(),
                           name='vendedor'),
)
