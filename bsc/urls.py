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

from bsc import views

urlpatterns = [

    url(r'^$', views.ScoreCardListView.as_view(), name='scorecard-index'),

    url(r'^(?P<pk>\d+)$', views.ScoreCardDetailView.as_view(),
        name='scorecard'),

    url(r'^user/(?P<pk>\d+)$', views.UserDetailView.as_view(),
        name='scorecard-user'),

    url(r'^encuestas$', views.EncuestaListView.as_view(), name='encuesta-list'),

    url(r'^soluciones$', views.SolucionListView.as_view(),
        name='solucion-list'),

    url(r'^encuesta/(?P<pk>\d+)$', views.EncuestaDetailView.as_view(),
        name='encuesta'),

    url(r'^encuesta/(?P<encuesta>\d+)/(?P<consulta>\d+)/responder$',
        views.RespuestaRedirectView.as_view(), name='encuesta-responder'),

    url(r'^encuesta/(?P<encuesta>\d+)/(?P<consulta>\d+)/encuestada$',
        views.ConsultaEncuestadaRedirectView.as_view(),
        name='encuesta-respondida'),

    url(r'^encuesta/(?P<encuesta>\d+)/(?P<consulta>\d+)/negada$',
        views.ConsultaNoEncuestadaRedirectView.as_view(),
        name='encuesta-no-respondida'),

    url(r'^solucion/(?P<solucion>\d+)/correo$',
        views.SolucionEmailView.as_view(),
        name='solucion-email'),

    url(r'^solucion/(?P<pk>\d+)/correo/preview$',
        views.SolucionEmailPreView.as_view(),
        name='solucion-email-preview'),

    url(r'^encuesta/(?P<encuesta>\d+)/(?P<consulta>\d+)/rellamar$',
        views.RellamarCreateView.as_view(),
        name='encuesta-rellamar'),

    url(r'^respuesta/(?P<pk>\d+)$', views.RespuestaDetailView.as_view(),
        name='respuesta'),

    url(r'^respuesta/(?P<respuesta>\d+)/votos/guardar$',
        views.save_votes, name='votos-guardar'),

    url(r'^voto/(?P<pk>\d+)/editar$', views.VotoUpdateView.as_view(),
        name='voto-editar'),

    url(r'^queja/(?P<respuesta>\d+)/agregar$', views.QuejaCreateView.as_view(),
        name='queja-agregar'),

    url(r'^quejas/$', views.QuejaListView.as_view(), name='quejas'),

    url(r'^queja/(?P<pk>\d+)$', views.QuejaDetailView.as_view(), name='queja'),

    url(r'^queja/(?P<queja>\d+)/solucion/agregar$',
        views.SolucionCreateView.as_view(), name='solucion-agregar'),

    url(r'^queja/solucion/(?P<pk>\d+)/aceptar$',
        views.SolucionAceptarUpdateView.as_view(), name='solucion-aceptar'),

    url(r'^queja/solucion/(?P<pk>\d+)/rechazar$',
        views.SolucionRechazarUpdateView.as_view(), name='solucion-rechazar'),

    url(r'^queja/(?P<queja>\d+)/solucion/l/agregar$',
        views.SolucionCreateView.as_view(), name='solucion-lista-agregar'),

    url(r'^notas/(?P<pk>\d+)$', views.ArchivoNotasDetailView.as_view(),
        name='archivonotas'),

    url(r'^notas/(?P<pk>\d+)/procesar$',
        views.ArchivoNotasProcesarView.as_view(),
        name='archivonotas-process'),

    url(r'^login/periodo', views.LoginPeriodoView.as_view(),
        name='login-periodo')

]
