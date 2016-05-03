# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from lab.views import IndexView, ResultadoCreateView
from persona.views import PersonaSearchView

urlpatterns = [

    url(r'^$',
        IndexView.as_view(),
        name='lab-index'),

    url(r'^resultado/(?P<persona>\d+)/agregar$',
        ResultadoCreateView.as_view(),
        name='lab-result-add'),

    url(r'^buscar$',
        PersonaSearchView.as_view(
                template_name='lab/persona_search.html'),
        name='lab-search'),

]
