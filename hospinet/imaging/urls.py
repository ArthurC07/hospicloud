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
from imaging.views import (ExamenDetailView, ExamenCreateView,
    ExamenUpdateView, ImagenCreateView, AdjuntoCreateView, ExamenIndexView,
    ExamenPersonaListView, PersonaExamenCreateView, ExamenPreCreateView,
    DicomDetailView, DicomCreateView, EstudioProgramadoListView,
    EstudioProgramadoCreateView, EstudioProgramadoEfectuarView,
    NotificarExamenView, EstudioPreCreateView, PersonaEstudioCreateView,
    EstudioProgramadoDetailView, EstudioCreateView)

urlpatterns = patterns('',
    
    url(r'^$',
        ExamenIndexView.as_view(),
        name='examen-index'),
    
    url(r'^(?P<pk>\d+)/notificar$',
        NotificarExamenView.as_view(),
        name='examen-notificar'),

    url(r'^persona/(?P<persona>\d+)$',
        EstudioProgramadoCreateView.as_view(),
        name='examen-programar'),

    url(r'^estudio/(?P<pk>\d+)$',
        EstudioProgramadoDetailView.as_view(),
        name='estudio-detail-view'),
    
    url(r'^estudio/(?P<pk>\d+)/efectuar$',
        EstudioProgramadoEfectuarView.as_view(),
        name='examen-efectuar'),
    
    url(r'^examenes$',
        ExamenIndexView.as_view(),
        name='examen-list'),
    
    url(r'^nuevo$',
        EstudioPreCreateView.as_view(),
        name='examen-nuevo'),

    url(r'^persona/nuevo$',
        PersonaEstudioCreateView.as_view(),
        name='examen-persona-nuevo'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        ExamenDetailView.as_view(),
        name='examen-view-id'),

    url(r'^(?P<pk>\d+)/editar$',
        ExamenUpdateView.as_view(),
        name='examen-edit'),
    
    url(r'^persona/(?P<pk>\d+)/lista$',
        ExamenPersonaListView.as_view(),
        name='examen-persona-lista'),
    
    url(r'^(?P<persona>\d+)/agregar$',
        ExamenCreateView.as_view(),
        name='examen-agregar'),
    
    url(r'^(?P<pk>\d+)/editar$',
        ExamenUpdateView.as_view(),
        name='examen-editar'),
    
    url(r'^(?P<examen>\d+)/imagen/adjuntar$',
        ImagenCreateView.as_view(),
        name='examen-adjuntar-imagen'),
    
    url(r'^(?P<examen>\d+)/archivo/adjuntar$',
        AdjuntoCreateView.as_view(),
        name='examen-adjuntar-archivo'),
    
    url(r'^(?P<examen>\d+)/dicom/adjuntar$',
        DicomCreateView.as_view(),
        name='examen-adjuntar-dicom'),
    
    url(r'^dicom/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        DicomDetailView.as_view(),
        name='dicom-view'),

    url(r'^(?P<examen>\d+)/estudio/agregar$',
        EstudioCreateView.as_view(),
        name='examen-estudio-create'),
)
