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
from clinique.views import (PacienteCreateView, PacienteDetailView,
                            ConsultorioIndexView, LecturaSignosCreateView,
                            EvaluacionCreateView, SeguimientoCreateView,
                            CitaCreateView, ConsultorioDetailView,
                            DiagnosticoCreateView, ConsultorioCreateView, ConsultaCreateView)

urlpatterns = patterns('',

                       url(r'^$',
                           ConsultorioIndexView.as_view(),
                           name='consultorio-index'),

                       url(r'^paciente/(?P<pk>\d+)$',
                           PacienteDetailView.as_view(),
                           name='clinique-paciente'),

                       url(r'^(?P<pk>\d+)$',
                           ConsultorioDetailView.as_view(),
                           name='consultorio'),

                       url(r'^agregar$',
                           ConsultorioCreateView.as_view(),
                           name='consultorio-agregar'),

                       url(
                           r'^(?P<persona>\d+)/(?P<consultorio>\d+)/paciente/agregar$',
                           PacienteCreateView.as_view(),
                           name='consultorio-paciente-agregar'),

                       url(r'^consulta/(?P<paciente>\d+)/agregar',
                           ConsultaCreateView.as_view(),
                           name='consultorio-consulta-agregar'),

                       url(r'^lectura/(?P<paciente>\d+)/agregar',
                           LecturaSignosCreateView.as_view(),
                           name='consultorio-lectura-agregar'),

                       url(r'^evaluacion/(?P<paciente>\d+)/agregar',
                           EvaluacionCreateView.as_view(),
                           name='consultorio-evaluacion-agregar'),

                       url(r'^seguimiento/(?P<paciente>\d+)/agregar',
                           SeguimientoCreateView.as_view(),
                           name='consultorio-segumiento-agregar'),

                       url(r'^cita/(?P<paciente>\d+)/agregar',
                           CitaCreateView.as_view(),
                           name='consultorio-cita-agregar'),

                       url(r'^diagnostico/(?P<paciente>\d+)/agregar',
                           DiagnosticoCreateView.as_view(),
                           name='consultorio-diagnostico-agregar'),
)
