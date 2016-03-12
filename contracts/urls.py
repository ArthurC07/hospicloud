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
from __future__ import unicode_literals

from django.conf.urls import url

from contracts import views

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='contrato-index'),

    url(r'^contrato/(?P<pk>\d+)$', views.ContratoDetailView.as_view(),
        name='contrato'),

    url(r'^plan/(?P<pk>\d+)$', views.PlanDetailView.as_view(),
        name='contracts-plan'),

    url(r'^plan/(?P<pk>\d+)/clone$',
        views.PlanCloneView.as_view(),
        name='contracts-plan-clone'),

    url(r'^plan/(?P<pk>\d+)/edit',
        views.PlanUpdateView.as_view(),
        name='contracts-plan-edit'),

    url(r'^plan/agregar$',
        views.PlanCreateView.as_view(),
        name='contracts-plan-add'),

    url(r'^precontrato/(?P<pk>\d+)$',
        views.PrecontratoDetailView.as_view(),
        name='precontrato'),

    url(r'^plan/buscar$', views.PlanSearchView.as_view(), name='plan-search'),

    url(r'^empresa/buscar$', views.EmpresaSearchView.as_view(),
        name='empresa-search'),

    url(r'^plan/(?P<plan>\d+)/beneficio/agregar$',
        views.BeneficioCreateView.as_view(),
        name='contracts-beneficio-add'),

    url(r'^plan/beneficio/(?P<pk>\d+)/edit$',
        views.BeneficioUpdateView.as_view(),
        name='contracts-beneficio-edit'),

    url(r'^(?P<plan>\d+)/limite/agregar$',
        views.LimiteEventoCreateView.as_view(),
        name='contracts-limite-add'),

    url(r'^(?P<plan>\d+)/beneficio/agregar$',
        views.BeneficioCreateView.as_view(),
        name='contracts-beneficio-add'),

    url(r'^(?P<persona>\d+)/contrato/agregar$',
        views.ContratoCreateView.as_view(),
        name='contrato-persona-add'),

    url(r'^(?P<persona>\d+)/master/contrato/agregar$',
        views.ContratoMasterPersonaCreateView.as_view(),
        name='contrato-persona-master-add'),

    url(r'^contrato/agregar$',
        views.ContratoPersonaCreateView.as_view(),
        name='contrato-add'),

    url(r'^precontrato/agregar$',
        views.PrecontratoCreateView.as_view(),
        name='precontrato-add'),

    url(r'^contrato/empresarial/agregar$',
        views.ContratoPersonaCreateView.as_view(),
        name='contrato-empresarial-add'),

    url(r'^contratos/beneficiarios$',
        views.ContratoBeneficiarioListView.as_view(),
        name='contrato-beneficiario-list'),

    url(r'^contratos$',
        views.ContratoListView.as_view(),
        name='contrato-list'),

    url(r'^contratos/empresariales$',
        views.ContratoEmpresarialListView.as_view(),
        name='contrato-empresarial-list'),

    url(r'^contrato/(?P<pk>\d+)/edit$',
        views.ContratoUpdateView.as_view(),
        name='contrato-edit'),

    url(r'^contrato/periodo',
        views.ContratoPeriodoView.as_view(),
        name='contrato-periodo'),

    url(r'^vendedor/periodo',
        views.VendedorPeriodoView.as_view(),
        name='vendedor-periodo'),

    url(r'^evento/periodo',
        views.EventoPeriodoView.as_view(),
        name='evento-periodo'),

    url(r'^contrato/buscar$',
        views.ContratoSearchView.as_view(),
        name='contrato-search'),

    url(r'^contrato/(?P<contrato>\d+)/pago/add$',
        views.PagoCreateView.as_view(),
        name='contrato-pago-add'),

    url(r'^contrato/(?P<contrato>\d+)/evento/add$',
        views.EventoCreateView.as_view(),
        name='contrato-evento-add'),

    url(r'^pago/(?P<pk>\d+)/delete$',
        views.PagoDeleteView.as_view(),
        name='contrato-pago-delete'),

    url(r'^pago/(?P<pk>\d+)/update$',
        views.PagoUpdateView.as_view(),
        name='contrato-pago-update'),

    url(r'^evento/(?P<pk>\d+)/delete$',
        views.EventoDeleteView.as_view(),
        name='contrato-evento-delete'),

    url(r'^beneficiario/(?P<pk>\d+)/delete$',
        views.BeneficiarioDeleteView.as_view(),
        name='contrato-beneficiario-delete'),

    url(r'^evento/(?P<pk>\d+)/update$',
        views.EventoUpdateView.as_view(),
        name='contrato-evento-update'),

    url(r'^vendedor/buscar$',
        views.VendedorSearchView.as_view(),
        name='vendedor-search'),

    url(r'^vendedor/add$',
        views.VendedorCreateView.as_view(),
        name='vendedor-add'),

    url(r'^vendedor/(?P<pk>\d+)$',
        views.VendedorDetailView.as_view(),
        name='contracts-vendedor'),

    url(r'^evento/tipo/add$',
        views.TipoEventoCreateView.as_view(),
        name='contrato-tipoevento-add'),

    url(r'^contrato/(?P<contrato>\d+)/beneficiario/add$',
        views.BeneficiarioPersonaCreateView.as_view(),
        name='contrato-beneficiario-add'),

    url(r'^contrato/(?P<pk>\d+)/prebeneficiario/add$',
        views.PrebeneficiarioCreateView.as_view(),
        name='contrato-prebeneficiario-add'),

    url(r'^(?P<persona>\d+)/beneficiario/agregar$',
        views.BeneficiarioCreateView.as_view(),
        name='persona-beneficiario-add'),

    url(r'^contrato/persona/buscar$',
        views.ContratoPersonaSearchView.as_view(),
        name='contrato-persona-search'),

    url(r'^meta/(?P<pk>\d+)$',
        views.MetaDetailView.as_view(),
        name='contracts-meta'),

    url(r'^meta/add$',
        views.MetaCreateView.as_view(),
        name='contracts-meta-add'),

    url(r'^contrato/(?P<contrato>\d+)/cancelar$',
        views.CancelacionCreateView.as_view(),
        name='contrato-cancelar'),

    url(r'^contrato/maestro/(?P<pk>\d+)$',
        views.MasterContractDetailView.as_view(),
        name='contract-master'),

    url(r'^contrato/maestro/(?P<pk>\d+)/edit$',
        views.MasterContractUpdateView.as_view(),
        name='contract-master-edit'),

    url(r'^contrato/maestro/list$',
        views.MasterContractListView.as_view(),
        name='contract-master-list'),

    url(r'^contrato/maestro/agregar$',
        views.MasterContractCreateView.as_view(),
        name='contracts-master-add'),

    url(r'^contrato/maestro/(?P<pk>\d+)/procesar$',
        views.MasterContractProcessView.as_view(),
        name='contracts-master-process'),

    url(r'^archivo/(?P<pk>\d+)$',
        views.ImportFileDetailView.as_view(),
        name='contracts-archivo'),

    url(r'^archivo/agregar$',
        views.ImportFileCreateView.as_view(),
        name='contracts-archivo-add'),

    url(r'^archivo/lista$',
        views.ImportFileListView.as_view(),
        name='contracts-archivo-list'),

    url(r'^archivo/(?P<pk>\d+)/procesar$',
        views.ImportFileProcessView.as_view(),
        name='contracts-archivo-process'),

    url(r'^pcd/(?P<pk>\d+)/editar$',
        views.PCDUpdateView.as_view(),
        name='contracts-pcd-editar'),

    url(r'^aseguradora/agregar$',
        views.AseguradoraCreateView.as_view(),
        name='contracts-aseguradora-add'),

    url(r'^aseguradora/(?P<pk>\d+)/editar$',
        views.AseguradoraUpdateView.as_view(),
        name='aseguradora-editar'),

    url(r'^aseguradora/(?P<pk>\d+)$',
        views.AseguradoraDetailView.as_view(),
        name='aseguradora'),
]
