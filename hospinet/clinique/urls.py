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
                            DiagnosticoCreateView, ConsultorioCreateView,
                            ConsultaCreateView, NotaEnfermeriaCreateView,
                            CliniquePersonaUpdateView, CliniqueFisicoUpdateView,
                            CliniqueEstiloVidaUpdateView, CitaListView,
                            CliniqueAntecedenteUpdateView, CargoCreateView,
                            CliniqueAntecedenteFamiliarUpdateView,
                            CliniqueAntecedenteQuirurgicoUpdateView,
                            CliniqueAntecedenteObstetricoUpdateView,
                            CliniqueAntecedenteQuirurgicoCreateView,
                            CitaPersonaCreateView, OrdenMedicaCreateView)


urlpatterns = patterns('',

                       url(r'^$',
                           ConsultorioIndexView.as_view(),
                           name='consultorio-index'),

                       url(r'^paciente/(?P<pk>\d+)$',
                           PacienteDetailView.as_view(),
                           name='clinique-paciente'),

                       url(r'^paciente/(?P<pk>\d+)/resume$',
                           PacienteDetailView.as_view(
                               template_name='clinique/clinique_detail.html'),
                           name='clinique-paciente-resume'),

                       url(r'^paciente/(?P<pk>\d+)/cargos',
                           PacienteDetailView.as_view(
                               template_name='clinique/cargo_list.html'),
                           name='clinique-cargos'),

                       url(r'^paciente/(?P<pk>\d+)/ordenes',
                           PacienteDetailView.as_view(
                               template_name='clinique/ordenes_list.html'),
                           name='clinique-ordenes'),

                       url(r'^paciente/(?P<pk>\d+)/signos',
                           PacienteDetailView.as_view(
                               template_name='clinique/signos_list.html'),
                           name='clinique-signos'),

                       url(r'^paciente/(?P<pk>\d+)/notas',
                           PacienteDetailView.as_view(
                               template_name='clinique/nota_list.html'),
                           name='clinique-notas'),

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

                       url(r'^consulta/(?P<paciente>\d+)/agregar$',
                           ConsultaCreateView.as_view(),
                           name='consultorio-consulta-agregar'),

                       url(r'^(?P<paciente>\d+)/nota/agregar$',
                           NotaEnfermeriaCreateView.as_view(),
                           name='consultorio-nota-agregar'),

                       url(
                           r'^lectura/(?P<persona>\d+)/(?P<consultorio>\d+)/agregar$',
                           LecturaSignosCreateView.as_view(),
                           name='consultorio-lectura-agregar'),

                       url(r'^evaluacion/(?P<paciente>\d+)/agregar$',
                           EvaluacionCreateView.as_view(),
                           name='consultorio-evaluacion-agregar'),

                       url(r'^seguimiento/(?P<paciente>\d+)/agregar$',
                           SeguimientoCreateView.as_view(),
                           name='consultorio-segumiento-agregar'),

                       url(r'^cita/agregar$',
                           CitaCreateView.as_view(),
                           name='consultorio-cita-agregar'),

                       url(r'^cita/(?P<persona>\d+)/agregar',
                           CitaPersonaCreateView.as_view(),
                           name='consultorio-citapersona-agregar'),

                       url(r'^cita/(?P<consultorio>\d+)$',
                           CitaListView.as_view(),
                           name='consultorio-cita-list'),

                       url(r'^diagnostico/(?P<paciente>\d+)/agregar$',
                           DiagnosticoCreateView.as_view(),
                           name='consultorio-diagnostico-agregar'),

                       url(r'^profile/persona/(?P<pk>\d+)/editar$',
                           CliniquePersonaUpdateView.as_view(),
                           name='clinique-persona-edit'),

                       url(r'^(?P<pk>\d+)/fisico/editar$',
                           CliniqueFisicoUpdateView.as_view(),
                           name='clinique-fisico-editar'),

                       url(r'^(?P<pk>\d+)/estilovida/editar$',
                           CliniqueEstiloVidaUpdateView.as_view(),
                           name='clinique-estilovida-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/editar$',
                           CliniqueAntecedenteUpdateView.as_view(),
                           name='clinique-antecedente-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
                           CliniqueAntecedenteFamiliarUpdateView.as_view(),
                           name='clinique-antecedente-familiar-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
                           CliniqueAntecedenteQuirurgicoUpdateView.as_view(),
                           name='clinique-antecedente-quirurgico-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
                           CliniqueAntecedenteObstetricoUpdateView.as_view(),
                           name='clinique-antecedente-obstetrico-editar'),

                       url(
                           r'^(?P<paciente>\d+)/(?P<persona>\d+)/antecedente/quirurgico/agregar$',
                           CliniqueAntecedenteQuirurgicoCreateView.as_view(),
                           name='clinique-antecedente-quirurgico-agregar'),

                       url(r'^(?P<paciente>\d+)/ordenmedica/agregar$',
                           OrdenMedicaCreateView.as_view(),
                           name='consultorio-om-agregar'),

                       url(r'^(?P<paciente>\d+)/cargo/agregar$',
                           CargoCreateView.as_view(),
                           name='consultorio-cargo-agregar'),
)
