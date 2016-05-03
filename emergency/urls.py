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

from emergency import views
from persona.views import PersonaDetailView

urlpatterns = [
    
    url(r'^$',
        views.EmergenciaIndexView.as_view(),
        name='emergency-index'),
    
    url(r'^ingresar$',
        views.EmergenciaPreCreateView.as_view(),
        name='emergency-ingresar'),

    url(r'^persona/ingresar$',
        views.PersonaEmergenciaCreateView.as_view(),
        name='emergency-persona-create'),

    url(r'^persona/(?P<pk>\d+)/lista$',
        PersonaDetailView.as_view(template_name='emergency/emergencia_persona_list.html'),
        name='emergency-persona-list'),

    url(r'^persona/(?P<persona>\d+)$',
        views.EmergenciaCreateView.as_view(),
        name='emergency-create'),

    url(r'^(?P<pk>\d+)/edit$',
        views.EmergenciaUpdateView.as_view(),
        name='emergencia-update'),

    url(r'^(?P<pk>\d+)$',
        views.EmergenciaDetailView.as_view(),
        name='emergency-view-id'),
    
    url(r'^(?P<emergencia>\d+)/tratamiento/agregar$',
        views.TratamientoCreateView.as_view(),
        name='emergencia-tratamiento-agregar'),
    
    url(r'^(?P<emergencia>\d+)/diagnostico/agregar$',
        views.DiagnosticoCreateView.as_view(),
        name='emergencia-diagnostico-agregar'),
    
    url(r'^(?P<emergencia>\d+)/hallazgo/agregar$',
        views.HallazgoCreateView.as_view(),
        name='emergencia-hallazgo-agregar'),
    
    url(r'^(?P<emergencia>\d+)/examenfisico/agregar$',
        views.ExamenFisicoCreateView.as_view(),
        name='emergencia-examen-fisico-agregar'),
    
    url(r'^(?P<emergencia>\d+)/remision/interna/agregar$',
        views.RemisionInternaCreateView.as_view(),
        name='emergencia-remision-interna-agregar'),

    url(r'^(?P<emergencia>\d+)/cobro/agregar$',
        views.CobroCreateView.as_view(),
        name='emergencia-cobro-agregar'),
    
    url(r'^cobro/(?P<pk>\d+)/eliminar$',
        views.CobroDeleteView.as_view(),
        name='emergencia-cobro-eliminar'),
    
    url(r'^(?P<emergencia>\d+)/remision/externa/agregar$',
        views.RemisionExternaCreateView.as_view(),
        name='emergencia-remision-externa-agregar'),

    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/fisico/editar$',
        views.EmergenciaFisicoUpdateView.as_view(),
        name='emergencia-fisico-editar'),
    
    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/antecedente/editar$',
        views.EmergenciaAntecedenteUpdateView.as_view(),
        name='emergencia-antecedente-editar'),
    
    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/antecedente/familiar/editar$',
        views.EmergenciaAntecedenteFamiliarUpdateView.as_view(),
        name='emergencia-antecedente-familiar-editar'),
    
    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/antecedente/obstetrico/editar$',
        views.EmergenciaAntecedenteObstetricoUpdateView.as_view(),
        name='emergencia-antecedente-obstetrico-editar'),

    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/antecedente/quirurgico/editar$',
        views.EmergenciaAntecedenteQuirurgicoUpdateView.as_view(),
        name='emergencia-antecedente-quirurgico-editar'),

    url(r'^(?P<pk>\d+)/(?P<emergencia>\d+)/antecedente/quirurgico/agregar$',
        views.EmergenciaAntecedenteQuirurgicoCreateView.as_view(),
        name='emergencia-antecedente-quirurgico-agregar'),
]
