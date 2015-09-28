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
from spital.views import (AdmisionIndexView, PersonaAdmisionCreateView,
    AdmisionCreateView, IngresarView, AdmisionDetailView, AutorizarView,
    FiadorAgregarView, ReferenciaAgregarView, PersonaFiadorCreateView,
    PersonaReferenciaCreateView, HospitalizarView, PagarView,
    HabitacionCreateView, HabitacionDetailView, HabitacionUpdateView,
    HabitacionListView, PreAdmisionCreateView, AdmisionPreCreateView, AdmisionDeleteView,
    DepositoCreateView, DepositoUpdateView, PreAdmisionDeleteView)

urlpatterns = patterns('',
    
    url(r'^$',
        AdmisionIndexView.as_view(),
        name='admision-index'),
    
    url(r'^(?P<pk>\d+)$',
        AdmisionDetailView.as_view(),
        name='admision-view-id'),

    url(r'^(?P<pk>\d+)/eliminar$',
        AdmisionDeleteView.as_view(),
        name='admision-delete'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        AdmisionDetailView.as_view(),
        name='admision-view-slug'),
    
    url(r'^(?P<pk>\d+)/autorizacion$',
        AdmisionDetailView.as_view(template_name="admision/autorizacion.html"),
        name='admision-autorizacion'),
    
    url(r'^(?P<pk>\d+)/fiadores$',
        AdmisionDetailView.as_view(template_name="admision/admision_fiadores.html"),
        name='admision-fiadores'),
    
    url(r'^(?P<admision>\d+)/fiadores/agregar$',
        PersonaFiadorCreateView.as_view(),
        name='admision-fiador'),
    
    url(r'^(?P<admision>\d+)/fiadores/agregar/(?P<persona>\d+)$',
        FiadorAgregarView.as_view(),
        name='admision-fiador-agregar'),
    
    url(r'^(?P<pk>\d+)/referencias$',
        AdmisionDetailView.as_view(template_name="admision/admision_referencias.html"),
        name='admision-referencias'),
    
    url(r'^(?P<admision>\d+)/referencias/agregar$',
        PersonaReferenciaCreateView.as_view(),
        name='admision-referencia'),
    
    url(r'^(?P<admision>\d+)/referencias/agregar/(?P<persona>\d+)$',
        ReferenciaAgregarView.as_view(),
        name='admision-referencia-agregar'),
    
    url(r'^(?P<pk>\d+)/autorizar$',
        AutorizarView.as_view(),
        name='admision-autorizar'),
    
    url(r'^(?P<pk>\d+)/hospitalizar$',
        HospitalizarView.as_view(),
        name='admision-hospitalizar'),
    
    url(r'^(?P<pk>\d+)/pagar$',
        PagarView.as_view(),
        name='admision-pagar'),
    
    url(r'^ingresar$',
        IngresarView.as_view(),
        name='admision-iniciar'),
    
    url(r'^persona/ingresar$',
        PersonaAdmisionCreateView.as_view(),
        name='admision-ingresar-persona'),
    
    url(r'^persona/(?P<persona>\d+)$',
        AdmisionCreateView.as_view(),
        name='admision-persona-agregar'),
    
    url(r'^habitacion$',
        HabitacionListView.as_view(),
        name='habitaciones'),

    url(r'^habitacion/agregar$',
        HabitacionCreateView.as_view(),
        name='habitacion-agregar'),
    
    url(r'^habitacion/(?P<pk>\d+)$',
        HabitacionDetailView.as_view(),
        name='habitacion-view'),
    
    url(r'^habitacion/(?P<pk>\d+)/editar$',
        HabitacionUpdateView.as_view(),
        name='habitacion-view'),
    
    url(r'^preadmision/(?P<emergencia>\d+)$',
        PreAdmisionCreateView.as_view(),
        name='preadmitir'),
    
    url(r'^preadmision/(?P<preadmision>\d+)/admitir$',
        AdmisionPreCreateView.as_view(),
        name='admitir-preadmision'),

    url(r'^preadmision/(?P<pk>\d+)/delete$',
        PreAdmisionDeleteView.as_view(),
        name='preadmision-delete'),

    url(r'^admision/(?P<pk>\d+)/delete$',
        AdmisionDeleteView.as_view(),
        name='admision-delete'),

    url(r'^(?P<admision>\d+)/deposito/agregar$',
        DepositoCreateView.as_view(),
        name='admision-deposito-agregar'),

    url(r'^deposito/(?P<pk>\d+)/editar$',
        DepositoUpdateView.as_view(),
        name='deposito-edit'),
)
