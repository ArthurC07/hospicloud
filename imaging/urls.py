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

from imaging import views

urlpatterns = [

    url(r'^$',
        views.ExamenIndexView.as_view(),
        name='examen-index'),

    url(r'^(?P<persona>\d+)/agregar$',
        views.ExamenCreateView.as_view(),
        name='examen-agregar'),

    url(r'^(?P<pk>\d+)$',
        views.ExamenDetailView.as_view(),
        name='examen-view-id'),

    url(r'^(?P<pk>\d+)/editar$',
        views.ExamenUpdateView.as_view(),
        name='examen-edit'),

    url(r'^(?P<pk>\d+)/efectuar$',
        views.ExamenEfectuarView.as_view(),
        name='examen-efectuar'),

    url(r'^(?P<pk>\d+)/cancelar',
        views.ExamenCancelarView.as_view(),
        name='examen-cancelar'),

    url(r'^(?P<pk>\d+)/notificar$',
        views.NotificarExamenView.as_view(),
        name='examen-notificar'),

    url(r'^list$',
        views.ExamenIndexView.as_view(),
        name='examen-list'),

    url(r'^nuevo$',
        views.EstudioPreCreateView.as_view(),
        name='examen-nuevo'),

    url(r'^persona/nuevo$',
        views.PersonaEstudioCreateView.as_view(),
        name='examen-persona-nuevo'),

    url(r'^persona/(?P<pk>\d+)/lista$',
        views.ExamenPersonaListView.as_view(),
        name='examen-persona-lista'),

    url(r'^(?P<examen>\d+)/imagen/adjuntar$',
        views.ImagenCreateView.as_view(),
        name='examen-adjuntar-imagen'),

    url(r'^(?P<examen>\d+)/archivo/adjuntar$',
        views.AdjuntoCreateView.as_view(),
        name='examen-adjuntar-archivo'),

    url(r'^(?P<examen>\d+)/dicom/adjuntar$',
        views.DicomCreateView.as_view(),
        name='examen-adjuntar-dicom'),

    url(r'^dicom/^(?P<pk>\d+)$',
        views.DicomDetailView.as_view(),
        name='dicom-view'),

    url(r'^(?P<examen>\d+)/estudio/agregar$',
        views.EstudioCreateView.as_view(),
        name='examen-estudio-create'),
]
