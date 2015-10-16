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
from django.conf.urls import patterns, url

from bsc.views import ScoreCardDetailView, ScoreCardListView, UserDetailView, \
    EncuestaListView, EncuestaDetailView, RespuestaDetailView, VotoUpdateView, \
    RespuestaRedirectView, save_votes, ConsultaEncuestadaRedirectView, \
    QuejaCreateView

urlpatterns = patterns('',

                       url(r'^$',
                           ScoreCardListView.as_view(),
                           name='scorecard-index'),

                       url(r'^(?P<pk>\d+)$',
                           ScoreCardDetailView.as_view(),
                           name='scorecard'),

                       url(r'^user/(?P<pk>\d+)$',
                           UserDetailView.as_view(),
                           name='scorecard-user'),

                       url(r'^encuestas$',
                           EncuestaListView.as_view(),
                           name='encuesta-list'),

                       url(r'^encuesta/(?P<pk>\d+)$',
                           EncuestaDetailView.as_view(),
                           name='encuesta'),

                       url(
                           r'^encuesta/(?P<encuesta>\d+)/('
                           r'?P<consulta>\d+)/responder$',
                           RespuestaRedirectView.as_view(),
                           name='encuesta-responder'),

                       url(
                           r'^encuesta/(?P<encuesta>\d+)/('
                           r'?P<consulta>\d+)/encuestada$',
                           ConsultaEncuestadaRedirectView.as_view(),
                           name='encuesta-respondida'),

                       url(r'^respuesta/(?P<pk>\d+)$',
                           RespuestaDetailView.as_view(),
                           name='respuesta'),

                       url(r'^respuesta/(?P<respuesta>\d+)/votos/guardar$',
                           save_votes, name='votos-guardar'),

                       url(r'^voto/(?P<pk>\d+)/editar$',
                           VotoUpdateView.as_view(),
                           name='voto-editar'),

                       url(r'^queja/(?P<respuesta>\d+)/agregar$',
                           QuejaCreateView.as_view(),
                           name='queja-agregar'),
                       )
