# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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

from users import views

urlpatterns = [
    url(r'^profile/persona/add$',
        views.UserPersonaCreateView.as_view(),
        name='user-persona-create'),

    url(r'^profile/persona/(?P<pk>\d+)/editar$',
        views.UserPersonaUpdateView.as_view(),
        name='user-persona-edit'),

    url(r'^(?P<pk>\d+)/fisico/editar$',
        views.UserFisicoUpdateView.as_view(),
        name='user-fisico-edit'),

    url(r'^(?P<pk>\d+)/estilovida/editar$',
        views.UserEstiloVidaUpdateView.as_view(),
        name='user-estilovida-edit'),

    url(r'^(?P<pk>\d+)/antecedente/editar$',
        views.UserAntecedenteUpdateView.as_view(),
        name='user-antecedente-edit'),

    url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
        views.UserAntecedenteFamiliarUpdateView.as_view(),
        name='user-antecedente-familiar-edit'),

    url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
        views.UserAntecedenteQuirurgicoUpdateView.as_view(),
        name='user-antecedente-quirurgico-edit'),

    url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
        views.UserAntecedenteObstetricoUpdateView.as_view(),
        name='user-antecedente-obstetrico-edit'),

    url(r'^(?P<persona>\d+)/antecedente/quirurgico/agregar$',
        views.UserAntecedenteQuirurgicoCreateView.as_view(),
        name='user-antecedente-quirurgico-agregar'),
]
