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
                             VendedorSearchView, VendedorDetailView,
                             VendedorCreateView, ContratoPeriodoView,
                             ContratoSearchView, ContratoPersonaCreateView,
                             TipoEventoCreateView,
                             BeneficiarioPersonaCreateView,
                             BeneficiarioCreateView, ContratoPersonaSearchView,
                             PlanDetailView, LimiteEventoCreateView,
                             PlanSearchView, ContratoListView, MetaDetailView,
                             MetaCreateView, CancelacionCreateView,
                             EventoUpdateView,
                             ContratoEmpresarialPersonaCreateView,
                             ContratoEmpresarialListView, EmpresaSearchView,
                             ContratoBeneficiarioListView, EventoPeriodoView,
                             BeneficiarioDeleteView, PagoUpdateView,
                             VendedorPeriodoView)


urlpatterns = patterns('',

                       url(r'^$',
                           IndexView.as_view(),
                           name='contrato-index'),

                       url(r'^contrato/(?P<pk>\d+)$',
                           ContratoDetailView.as_view(),
                           name='contrato'),

                       url(r'^plan/(?P<pk>\d+)$',
                           PlanDetailView.as_view(),
                           name='contracts-plan'),

                       url(r'^plan/buscar$',
                           PlanSearchView.as_view(),
                           name='plan-search'),

                       url(r'^empresa/buscar$',
                           EmpresaSearchView.as_view(),
                           name='empresa-search'),

                       url(r'^(?P<plan>\d+)/limite/agregar$',
                           LimiteEventoCreateView.as_view(),
                           name='contracts-limite-add'),

                       url(r'^(?P<persona>\d+)/contrato/agregar$',
                           ContratoCreateView.as_view(),
                           name='contrato-persona-add'),

                       url(
                           r'^contrato/agregar$',
                           ContratoPersonaCreateView.as_view(),
                           name='contrato-add'),

                       url(
                           r'^contrato/empresarial/agregar$',
                           ContratoEmpresarialPersonaCreateView.as_view(),
                           name='contrato-empresarial-add'),

                       url(
                           r'^contratos/beneficiarios$',
                           ContratoBeneficiarioListView.as_view(),
                           name='contrato-beneficiario-list'),

                       url(
                           r'^contratos$',
                           ContratoListView.as_view(),
                           name='contrato-list'),

                       url(
                           r'^contratos/empresariales$',
                           ContratoEmpresarialListView.as_view(),
                           name='contrato-empresarial-list'),

                       url(r'^contrato/(?P<pk>\d+)/edit$',
                           ContratoUpdateView.as_view(),
                           name='contrato-edit'),

                       url(r'^contrato/periodo',
                           ContratoPeriodoView.as_view(),
                           name='contrato-periodo'),

                       url(r'^vendedor/periodo',
                           VendedorPeriodoView.as_view(),
                           name='vendedor-periodo'),

                       url(r'^evento/periodo',
                           EventoPeriodoView.as_view(),
                           name='evento-periodo'),

                       url(r'^contrato/buscar$',
                           ContratoSearchView.as_view(),
                           name='contrato-search'),

                       url(r'^contrato/(?P<contrato>\d+)/pago/add$',
                           PagoCreateView.as_view(),
                           name='contrato-pago-add'),

                       url(r'^contrato/(?P<contrato>\d+)/evento/add$',
                           EventoCreateView.as_view(),
                           name='contrato-evento-add'),

                       url(r'^pago/(?P<pk>\d+)/delete$',
                           PagoDeleteView.as_view(),
                           name='contrato-pago-delete'),

                       url(r'^pago/(?P<pk>\d+)/update$',
                           PagoUpdateView.as_view(),
                           name='contrato-pago-update'),

                       url(r'^evento/(?P<pk>\d+)/delete$',
                           EventoDeleteView.as_view(),
                           name='contrato-evento-delete'),

                       url(r'^beneficiario/(?P<pk>\d+)/delete$',
                           BeneficiarioDeleteView.as_view(),
                           name='contrato-beneficiario-delete'),

                       url(r'^evento/(?P<pk>\d+)/update$',
                           EventoUpdateView.as_view(),
                           name='contrato-evento-update'),

                       url(r'^vendedor/buscar$',
                           VendedorSearchView.as_view(),
                           name='vendedor-search'),

                       url(r'^vendedor/add$',
                           VendedorCreateView.as_view(),
                           name='vendedor-add'),

                       url(r'^vendedor/(?P<pk>\d+)$',
                           VendedorDetailView.as_view(),
                           name='contracts-vendedor'),

                       url(r'^evento/tipo/add$',
                           TipoEventoCreateView.as_view(),
                           name='contrato-tipoevento-add'),

                       url(r'^contrato/(?P<contrato>\d+)/beneficiario/add$',
                           BeneficiarioPersonaCreateView.as_view(),
                           name='contrato-beneficiario-add'),


                       url(r'^(?P<persona>\d+)/beneficiario/agregar$',
                           BeneficiarioCreateView.as_view(),
                           name='persona-beneficiario-add'),

                       url(r'^contrato/persona/buscar$',
                           ContratoPersonaSearchView.as_view(),
                           name='contrato-persona-search'),

                       url(r'^meta/(?P<pk>\d+)$',
                           MetaDetailView.as_view(),
                           name='contracts-meta'),

                       url(r'^meta/add$',
                           MetaCreateView.as_view(),
                           name='contracts-meta-add'),

                       url(r'^contrato/(?P<contrato>\d+)/cancelar$',
                           CancelacionCreateView.as_view(),
                           name='contrato-cancelar'),
)
