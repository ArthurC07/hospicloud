# -*- coding: utf-8 -*-
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
from persona.views import (PersonaDetailView, PersonaCreateView,
                           PersonaUpdateView, EstiloVidaUpdateView,
                           AntecedenteUpdateView,
                           AntecedenteFamiliarUpdateView,
                           AntecedenteObstetricoUpdateView,
                           PersonaIndexView, FisicoUpdateView,
                           AntecedenteQuirurgicoUpdateView,
                           AntecedenteQuirurgicoCreateView, PersonaSearchView,
                           EmpleoCreateView, PersonaDuplicateView,
                           EmpleadorDetailView, EmpleadorCreateView)

urlpatterns = patterns('',

                       url(r'^$',
                           PersonaIndexView.as_view(),
                           name='persona-index'),

                       url(r'^(?P<pk>\d+)$',
                           PersonaDetailView.as_view(),
                           name='persona-view-id'),

                       url(r'^(?P<pk>\d+)/estilovida$',
                           PersonaDetailView.as_view(
                               template_name='persona/estilo_detail.html'),
                           name='persona-estilo'),

                       url(r'^agregar$',
                           PersonaCreateView.as_view(),
                           name='persona-create'),

                       url(r'^empresa/(?P<pk>\d+)$',
                           EmpleadorDetailView.as_view(),
                           name='empresa'),

                       url(r'^empresa/agregar$',
                           EmpleadorCreateView.as_view(),
                           name='empresa-add'),

                       url(r'^buscar$',
                           PersonaSearchView.as_view(),
                           name='persona-search'),

                       url(r'^(?P<pk>\d+)/editar$',
                           PersonaUpdateView.as_view(),
                           name='persona-editar'),

                       url(r'^(?P<pk>\d+)/duplicada$',
                           PersonaDuplicateView.as_view(),
                           name='persona-duplicate'),

                       url(r'^(?P<persona>\d+)/empleo/add$',
                           EmpleoCreateView.as_view(),
                           name='persona-empleo-add'),

                       url(r'^(?P<pk>\d+)/fisico/editar$',
                           FisicoUpdateView.as_view(),
                           name='persona-fisico-editar'),

                       url(r'^(?P<pk>\d+)/estilovida/editar$',
                           EstiloVidaUpdateView.as_view(),
                           name='persona-estilovida-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/editar$',
                           AntecedenteUpdateView.as_view(),
                           name='persona-antecedente-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
                           AntecedenteFamiliarUpdateView.as_view(),
                           name='persona-antecedente-familiar-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
                           AntecedenteQuirurgicoUpdateView.as_view(),
                           name='persona-antecedente-quirurgico-editar'),

                       url(r'^(?P<persona>\d+)/antecedente/quirurgico/agregar$',
                           AntecedenteQuirurgicoCreateView.as_view(),
                           name='persona-antecedente-quirurgico-agregar'),

                       url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
                           AntecedenteObstetricoUpdateView.as_view(),
                           name='persona-antecedente-obstetrico-editar'),
)
