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
                            CitaPersonaCreateView, OrdenMedicaCreateView,
                            EsperaCreateView, EsperaAusenteView,
                            CitaAusenteView, PacientePersonaCreateView,
                            CitaPeriodoView, PacienteSearchView,
                            LecturaSignosUpdateView, DiagnosticoUpdateView,
                            ExamenUpdateView, OrdenMedicaUpdateView,
                            EvaluacionUpdateView, PrescripcionUpdateView,
                            PrescripcionCreateView, PacienteDeleteView,
                            DiagnosticoPeriodoView, CargoPeriodoView,
                            EvaluacionPeriodoView, IncapacidadCreateView,
                            SeguimientoPeriodoView, ConsultorioPacienteListView,
                            CliniqueAntecedenteObstetricoCreateView,
                            ReporteCreateView, CitaEsperaRedirectView,
                            RemisionCreateView, EsperaConsultaRedirectView,
                            EsperaTerminadaRedirectView, ConsultaDetailView,
                            ConsultaTerminadaRedirectView,
                            IncapacidadUpdateView, EsperaConsultorioCreateView,
                            ConsultaPeriodoView)


urlpatterns = patterns('',

                       url(r'^$',
                           ConsultorioIndexView.as_view(),
                           name='consultorio-index'),

                       url(r'^paciente/(?P<pk>\d+)$',
                           PacienteDetailView.as_view(),
                           name='clinique-paciente'),

                       url(r'^paciente/(?P<pk>\d+)/delete$',
                           PacienteDeleteView.as_view(),
                           name='clinique-paciente-delete'),

                       url(r'^paciente/(?P<pk>\d+)/resume$',
                           PacienteDetailView.as_view(
                               template_name='clinique/clinique_detail.html'),
                           name='clinique-paciente-resume'),

                       url(r'^paciente/(?P<pk>\d+)/cargos$',
                           PacienteDetailView.as_view(
                               template_name='clinique/cargo_list.html'),
                           name='clinique-cargos'),

                       url(r'^paciente/(?P<pk>\d+)/ordenes$',
                           PacienteDetailView.as_view(
                               template_name='clinique/ordenes_list.html'),
                           name='clinique-ordenes'),

                       url(r'^paciente/(?P<pk>\d+)/signos$',
                           PacienteDetailView.as_view(
                               template_name='clinique/signos_list.html'),
                           name='clinique-signos'),

                       url(r'^signos/(?P<pk>\d+)/editar$',
                           LecturaSignosUpdateView.as_view(),
                           name='clinique-signos-edit'),

                       url(r'^diagnostico/(?P<pk>\d+)/editar$',
                           DiagnosticoUpdateView.as_view(),
                           name='clinique-diagnostico-edit'),

                       url(r'^examen/(?P<pk>\d+)/editar$',
                           ExamenUpdateView.as_view(),
                           name='clinique-examen-edit'),

                       url(r'^evaluacion/(?P<pk>\d+)/editar$',
                           EvaluacionUpdateView.as_view(),
                           name='clinique-evaluacion-edit'),

                       url(r'^orden/(?P<pk>\d+)/editar$',
                           OrdenMedicaUpdateView.as_view(),
                           name='clinique-orden-edit'),

                       url(r'^paciente/(?P<pk>\d+)/notas$',
                           PacienteDetailView.as_view(
                               template_name='clinique/nota_list.html'),
                           name='clinique-notas'),

                       url(r'^(?P<pk>\d+)$',
                           ConsultorioDetailView.as_view(),
                           name='consultorio'),

                       url(r'^(?P<consultorio>\d+)/pacientes$',
                           ConsultorioPacienteListView.as_view(),
                           name='consultorio-pacientes'),

                       url(r'^agregar$',
                           ConsultorioCreateView.as_view(),
                           name='consultorio-agregar'),

                       url(
                           r'^consultorio/(?P<consultorio>\d+)/paciente/agregar$',
                           PacientePersonaCreateView.as_view(),
                           name='consultorio-persona-agregar'),

                       url(
                           r'^consultorio/(?P<consultorio>\d+)/reporte/agregar$',
                           ReporteCreateView.as_view(),
                           name='consultorio-report-agregar'),

                       url(
                           r'^(?P<persona>\d+)/(?P<consultorio>\d+)/paciente/agregar$',
                           PacienteCreateView.as_view(),
                           name='consultorio-paciente-agregar'),

                       url(r'^consulta/(?P<pk>\d+)$',
                           ConsultaDetailView.as_view(),
                           name='consulta'),

                       url(r'^consulta/periodo$',
                           ConsultaPeriodoView.as_view(),
                           name='consulta-periodo'),

                       url(
                           r'^(?P<persona>\d+)/consultorio/agregar$',
                           PacienteCreateView.as_view(),
                           name='consultorio-paciente-add'),

                       url(r'^consulta/(?P<persona>\d+)/(?P<consultorio>\d+)/agregar$',
                           ConsultaCreateView.as_view(),
                           name='consultorio-consulta-agregar'),

                       url(r'^(?P<persona>\d+)/nota/agregar$',
                           NotaEnfermeriaCreateView.as_view(),
                           name='consultorio-nota-agregar'),

                       url(
                           r'^lectura/(?P<persona>\d+)/agregar$',
                           LecturaSignosCreateView.as_view(),
                           name='consultorio-lectura-agregar'),

                       url(r'^evaluacion/(?P<persona>\d+)/(?P<consulta>\d+)/agregar$',
                           EvaluacionCreateView.as_view(),
                           name='consultorio-evaluacion-agregar'),

                       url(r'^seguimiento/(?P<persona>\d+)/agregar$',
                           SeguimientoCreateView.as_view(),
                           name='consultorio-segumiento-agregar'),

                       url(r'^cita/agregar$',
                           CitaCreateView.as_view(),
                           name='consultorio-cita-agregar'),

                       url(r'^cita/(?P<persona>\d+)/agregar$',
                           CitaPersonaCreateView.as_view(),
                           name='consultorio-citapersona-agregar'),

                       url(r'^cita/(?P<consultorio>\d+)$',
                           CitaListView.as_view(),
                           name='consultorio-cita-list'),

                       url(r'^(?P<pk>\d+)/cita/ausente$',
                           CitaAusenteView.as_view(),
                           name='clinique-cita-ausente'),

                       url(r'^cita/(?P<pk>\d+)/espera$',
                           CitaEsperaRedirectView.as_view(),
                           name='clinique-cita-espera'),

                       url(r'^espera/(?P<pk>\d+)/consulta$',
                           EsperaConsultaRedirectView.as_view(),
                           name='clinique-espera-consulta'),

                       url(r'^espera/(?P<pk>\d+)/terminada$',
                           EsperaTerminadaRedirectView.as_view(),
                           name='clinique-espera-terminada'),

                       url(r'^consulta/(?P<pk>\d+)/terminada$',
                           ConsultaTerminadaRedirectView.as_view(),
                           name='clinique-consulta-terminada'),

                       url(r'^diagnostico/(?P<persona>\d+)/(?P<consulta>\d+)/agregar$',
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

                       url(r'^(?P<persona>\d+)/antecedente/obstetrico/agregar',
                           CliniqueAntecedenteObstetricoCreateView.as_view(),
                           name='clinique-antecedente-obstetrico-agregar'),

                       url(
                           r'^(?P<paciente>\d+)/(?P<persona>\d+)/antecedente/quirurgico/agregar$',
                           CliniqueAntecedenteQuirurgicoCreateView.as_view(),
                           name='clinique-antecedente-quirurgico-agregar'),

                       url(r'^(?P<persona>\d+)/(?P<consulta>\d+)/ordenmedica/agregar$',
                           OrdenMedicaCreateView.as_view(),
                           name='consultorio-om-agregar'),

                       url(r'^(?P<consulta>\d+)/cargo/agregar$',
                           CargoCreateView.as_view(),
                           name='consultorio-cargo-agregar'),

                       url(
                           r'^(?P<persona>\d+)/(?P<consultorio>\d+)/espera/agregar$',
                           EsperaCreateView.as_view(),
                           name='consultorio-espera-agregar'),

                       url(
                           r'^(?P<persona>\d+)/espera/agregar$',
                           EsperaConsultorioCreateView.as_view(),
                           name='consultorio-espera-u-agregar'),

                       url(r'^(?P<pk>\d+)/espera/ausente$',
                           EsperaAusenteView.as_view(),
                           name='clinique-espera-ausente'),

                       url(r'^cita/periodo$',
                           CitaPeriodoView.as_view(),
                           name='cita-periodo'),

                       url(r'^diagnostico/periodo$',
                           DiagnosticoPeriodoView.as_view(),
                           name='diagnostico-periodo'),

                       url(r'^cargo/periodo$',
                           CargoPeriodoView.as_view(),
                           name='cargo-periodo'),

                       url(r'^evaluacion/periodo$',
                           EvaluacionPeriodoView.as_view(),
                           name='evaluacion-periodo'),

                       url(r'^seguimiento/periodo$',
                           SeguimientoPeriodoView.as_view(),
                           name='seguimiento-periodo'),

                       url(r'^paciente/search$',
                           PacienteSearchView.as_view(),
                           name='clinique-paciente-search'),

                       url(r'^paciente/search/add$',
                           PacienteSearchView.as_view(
                               template_name='clinique/paciente_add_list.html'),
                           name='clinique-paciente-search-add'),

                       url(r'^(?P<persona>\d+)/(?P<consulta>\d+)/prescripcion/agregar$',
                           PrescripcionCreateView.as_view(),
                           name='consultorio-prescripcion-agregar'),

                       url(r'^prescripcion/(?P<pk>\d+)/editar$',
                           PrescripcionUpdateView.as_view(),
                           name='clinique-prescripcion-edit'),

                       url(r'^(?P<persona>\d+)/(?P<consulta>\d+)/incapacidad/agregar$',
                           IncapacidadCreateView.as_view(),
                           name='consultorio-incapacidad-agregar'),

                       url(r'^incapacidad/(?P<pk>\d+)/editar$',
                           IncapacidadUpdateView.as_view(),
                           name='clinique-incapacidad-edit'),

                       url(
                           r'^(?P<persona>\d+)/remision/agregar$',
                           RemisionCreateView.as_view(),
                           name='consultorio-remision-agregar'),
)
