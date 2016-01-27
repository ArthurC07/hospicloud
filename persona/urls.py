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
from __future__ import unicode_literals

from django.conf.urls import url

from persona import views

urlpatterns = [
    url(r'^$',
        views.PersonaIndexView.as_view(),
        name='persona-index'),

    url(r'^(?P<pk>\d+)$',
        views.PersonaDetailView.as_view(),
        name='persona-view-id'),

    url(r'^(?P<pk>\d+)/estilovida$',
        views.PersonaDetailView.as_view(
                template_name='persona/estilo_detail.html'),
        name='persona-estilo'),

    url(r'^agregar$',
        views.PersonaCreateView.as_view(),
        name='persona-create'),

    url(r'^persona/duplicados/limpiar$',
        views.PersonaDuplicateRemoveView.as_view(),
        name='persona-duplicate-clean'),

    url(r'^empresa/(?P<pk>\d+)$',
        views.EmpleadorDetailView.as_view(),
        name='empresa'),

    url(r'^empresa/agregar$',
        views.EmpleadorCreateView.as_view(),
        name='empresa-add'),

    url(r'^buscar$',
        views.PersonaSearchView.as_view(),
        name='persona-search'),

    url(r'^(?P<pk>\d+)/editar$',
        views.PersonaUpdateView.as_view(),
        name='persona-editar'),

    url(r'^(?P<pk>\d+)/duplicada$',
        views.PersonaDuplicateView.as_view(),
        name='persona-duplicate'),

    url(r'^(?P<persona>\d+)/empleo/add$',
        views.EmpleoCreateView.as_view(),
        name='persona-empleo-add'),

    url(r'^(?P<pk>\d+)/fisico/editar$',
        views.FisicoUpdateView.as_view(),
        name='persona-fisico-editar'),

    url(r'^(?P<pk>\d+)/estilovida/editar$',
        views.EstiloVidaUpdateView.as_view(),
        name='persona-estilovida-editar'),

    url(r'^(?P<pk>\d+)/antecedente/editar$',
        views.AntecedenteUpdateView.as_view(),
        name='persona-antecedente-editar'),

    url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
        views.AntecedenteFamiliarUpdateView.as_view(),
        name='persona-antecedente-familiar-editar'),

    url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
        views.AntecedenteQuirurgicoUpdateView.as_view(),
        name='persona-antecedente-quirurgico-editar'),

    url(r'^(?P<persona>\d+)/antecedente/quirurgico/agregar$',
        views.AntecedenteQuirurgicoCreateView.as_view(),
        name='persona-antecedente-quirurgico-agregar'),

    url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
        views.AntecedenteObstetricoUpdateView.as_view(),
        name='persona-antecedente-obstetrico-editar'),
]
