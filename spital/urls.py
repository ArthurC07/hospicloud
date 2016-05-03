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
from __future__ import unicode_literals

from django.conf.urls import url

from spital import views

urlpatterns = [

    url(r'^$',
        views.AdmisionIndexView.as_view(),
        name='admision-index'),

    url(r'^(?P<pk>\d+)$',
        views.AdmisionDetailView.as_view(),
        name='admision-view-id'),

    url(r'^(?P<pk>\d+)/eliminar$',
        views.AdmisionDeleteView.as_view(),
        name='admision-delete'),

    url(
        r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        views.AdmisionDetailView.as_view(),
        name='admision-view-slug'),

    url(r'^(?P<pk>\d+)/autorizacion$',
        views.AdmisionDetailView.as_view(
            template_name="admision/autorizacion.html"),
        name='admision-autorizacion'),

    url(r'^(?P<pk>\d+)/fiadores$',
        views.AdmisionDetailView.as_view(
            template_name="admision/admision_fiadores.html"),
        name='admision-fiadores'),

    url(r'^(?P<admision>\d+)/fiadores/agregar$',
        views.PersonaFiadorCreateView.as_view(),
        name='admision-fiador'),

    url(r'^(?P<admision>\d+)/fiadores/agregar/(?P<persona>\d+)$',
        views.FiadorAgregarView.as_view(),
        name='admision-fiador-agregar'),

    url(r'^(?P<pk>\d+)/referencias$',
        views.AdmisionDetailView.as_view(
            template_name="admision/admision_referencias.html"),
        name='admision-referencias'),

    url(r'^(?P<admision>\d+)/referencias/agregar$',
        views.PersonaReferenciaCreateView.as_view(),
        name='admision-referencia'),

    url(r'^(?P<admision>\d+)/referencias/agregar/(?P<persona>\d+)$',
        views.ReferenciaAgregarView.as_view(),
        name='admision-referencia-agregar'),

    url(r'^(?P<pk>\d+)/autorizar$',
        views.AutorizarView.as_view(),
        name='admision-autorizar'),

    url(r'^(?P<pk>\d+)/hospitalizar$',
        views.HospitalizarView.as_view(),
        name='admision-hospitalizar'),

    url(r'^(?P<pk>\d+)/pagar$',
        views.PagarView.as_view(),
        name='admision-pagar'),

    url(r'^ingresar$',
        views.IngresarView.as_view(),
        name='admision-iniciar'),

    url(r'^persona/ingresar$',
        views.PersonaAdmisionCreateView.as_view(),
        name='admision-ingresar-persona'),

    url(r'^persona/(?P<persona>\d+)$',
        views.AdmisionCreateView.as_view(),
        name='admision-persona-agregar'),

    url(r'^habitacion$',
        views.HabitacionListView.as_view(),
        name='habitaciones'),

    url(r'^habitacion/agregar$',
        views.HabitacionCreateView.as_view(),
        name='habitacion-agregar'),

    url(r'^habitacion/(?P<pk>\d+)$',
        views.HabitacionDetailView.as_view(),
        name='habitacion-view'),

    url(r'^habitacion/(?P<pk>\d+)/editar$',
        views.HabitacionUpdateView.as_view(),
        name='habitacion-view'),

    url(r'^preadmision/(?P<emergencia>\d+)$',
        views.PreAdmisionCreateView.as_view(),
        name='preadmitir'),

    url(r'^preadmision/(?P<preadmision>\d+)/admitir$',
        views.AdmisionPreCreateView.as_view(),
        name='admitir-preadmision'),

    url(r'^preadmision/(?P<pk>\d+)/delete$',
        views.PreAdmisionDeleteView.as_view(),
        name='preadmision-delete'),

    url(r'^admision/(?P<pk>\d+)/delete$',
        views.AdmisionDeleteView.as_view(),
        name='admision-delete'),

    url(r'^(?P<admision>\d+)/deposito/agregar$',
        views.DepositoCreateView.as_view(),
        name='admision-deposito-agregar'),

    url(r'^deposito/(?P<pk>\d+)/editar$',
        views.DepositoUpdateView.as_view(),
        name='deposito-edit'),
]
