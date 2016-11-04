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

from clinique import views

urlpatterns = [

    url(r'^$',
        views.ConsultorioIndexView.as_view(),
        name='consultorio-index'),

    url(r'^mensual$', views.ClinicalData.as_view(),
        name='clinique-monthly'),

    url(r'^paciente/(?P<pk>\d+)/resume$',
        views.PacienteDetailView.as_view(
                template_name='clinique/clinique_detail.html'),
        name='clinique-paciente-resume'),

    url(r'^paciente/(?P<pk>\d+)/cargos$',
        views.PacienteDetailView.as_view(
                template_name='clinique/cargo_list.html'),
        name='clinique-cargos'),

    url(r'^paciente/(?P<pk>\d+)/signos$',
        views.PacienteDetailView.as_view(
                template_name='clinique/signos_list.html'),
        name='clinique-signos'),

    url(r'^signos/(?P<pk>\d+)/editar$',
        views.LecturaSignosUpdateView.as_view(),
        name='clinique-signos-edit'),

    url(r'^diagnostico/(?P<pk>\d+)/editar$',
        views.DiagnosticoUpdateView.as_view(),
        name='clinique-diagnostico-edit'),

    url(r'^examen/(?P<pk>\d+)/editar$',
        views.ExamenUpdateView.as_view(),
        name='clinique-examen-edit'),

    url(r'^evaluacion/(?P<pk>\d+)/editar$',
        views.EvaluacionUpdateView.as_view(),
        name='clinique-evaluacion-edit'),

    url(r'^orden/(?P<pk>\d+)/editar$',
        views.OrdenMedicaUpdateView.as_view(),
        name='clinique-orden-edit'),

    url(r'^orden/list$',
        views.OrdenMedicaListView.as_view(),
        name='clinique-orden-list'),

    url(r'^(?P<pk>\d+)$',
        views.ConsultorioDetailView.as_view(),
        name='consultorio'),

    url(r'^agregar$',
        views.ConsultorioCreateView.as_view(),
        name='consultorio-agregar'),

    url(r'^esperas$',
        views.EsperaListView.as_view(),
        name='esperas'),

    url(r'^consultorio/(?P<consultorio>\d+)/reporte/agregar$',
        views.ReporteCreateView.as_view(),
        name='consultorio-report-agregar'),

    url(r'^consulta/(?P<pk>\d+)$',
        views.ConsultaDetailView.as_view(),
        name='consulta'),

    url(r'^consulta/periodo$',
        views.ConsultaPeriodoView.as_view(),
        name='consulta-periodo'),

    url(r'^consulta/frecuencia$',
        views.ConsultaFrecuenciaView.as_view(),
        name='consulta-frecuencia'),

    url(r'^consulta/frecuencia/ciudad/(?P<pk>\d+)$',
        views.ConsultaFrecuenciaCiudadView.as_view(),
        name='consulta-frecuencia-ciudad'),

    url(r'^aseguradora/(?P<pk>\d+)$',
        views.ConsultaAseguradoraPeriodoView.as_view(),
        name='consulta-aseguradora'),

    url(r'^enfermera/(?P<pk>\d+)$',
        views.ConsultaEnfermeraPeriodoView.as_view(),
        name='consulta-enfermera'),

    url(r'^medico/(?P<pk>\d+)$',
        views.ConsultaMedicoPeriodoView.as_view(),
        name='consulta-medico'),

    url(r'^ciudad/(?P<pk>\d+)$',
        views.ConsultaCiudadPeriodoView.as_view(),
        name='consulta-ciudad'),

    url(r'^aseguradora/periodo$',
        views.ConsultaAseguradoraPeriodoListView.as_view(),
        name='consulta-aseguradora-periodo'),

    url(r'^consulta/estadisticas$',
        views.ConsultaEstadisticaPeriodoListView.as_view(),
        name='consulta-estadisticas'),

    url(r'^consulta/(?P<persona>\d+)/(?P<consultorio>\d+)/agregar$',
        views.ConsultaCreateView.as_view(),
        name='consultorio-consulta-agregar'),

    url(r'^(?P<persona>\d+)/nota/agregar$',
        views.NotaEnfermeriaCreateView.as_view(),
        name='consultorio-nota-agregar'),

    url(r'^lectura/(?P<persona>\d+)/agregar$',
        views.LecturaSignosCreateView.as_view(),
        name='consultorio-lectura-agregar'),

    url(r'^evaluacion/(?P<persona>\d+)/(?P<consulta>\d+)/agregar$',
        views.EvaluacionCreateView.as_view(),
        name='consultorio-evaluacion-agregar'),

    url(r'^seguimiento/(?P<persona>\d+)/agregar$',
        views.SeguimientoCreateView.as_view(),
        name='consultorio-segumiento-agregar'),

    url(r'^cita/agregar$',
        views.CitaCreateView.as_view(),
        name='consultorio-cita-agregar'),

    url(r'^cita/(?P<persona>\d+)/agregar$',
        views.CitaPersonaCreateView.as_view(),
        name='consultorio-citapersona-agregar'),

    url(r'^cita/(?P<consultorio>\d+)$',
        views.CitaListView.as_view(),
        name='consultorio-cita-list'),

    url(r'^(?P<pk>\d+)/cita/ausente$',
        views.CitaAusenteView.as_view(),
        name='clinique-cita-ausente'),

    url(r'^cita/(?P<pk>\d+)/espera$',
        views.CitaEsperaRedirectView.as_view(),
        name='clinique-cita-espera'),

    url(r'^espera/(?P<pk>\d+)/consulta$',
        views.EsperaConsultaRedirectView.as_view(),
        name='clinique-espera-consulta'),

    url(r'^espera/(?P<pk>\d+)/editar$',
        views.EsperaUpdateView.as_view(),
        name='clinique-espera-editar'),

    url(r'^espera/(?P<pk>\d+)/terminada$',
        views.EsperaTerminadaRedirectView.as_view(),
        name='clinique-espera-terminada'),

    url(r'^espera/(?P<espera>\d+)/consulta/iniciar$',
        views.ConsultaEsperaCreateView.as_view(),
        name='espera-consulta-iniciar'),

    url(r'^consulta/(?P<pk>\d+)/terminada$',
        views.ConsultaTerminadaRedirectView.as_view(),
        name='clinique-consulta-terminada'),

    url(r'^consulta/(?P<pk>\d+)/revisar$',
        views.ConsultaRevisarView.as_view(),
        name='clinique-consulta-revisar'),

    url(r'^afecciones$',
        views.AfeccionAutoComplete.as_view(),
        name='afecciones'),

    url(r'^diagnostico/(?P<persona>\d+)/(?P<consulta>\d+)/buscar$',
        views.AfecionesSearchView.as_view(),
        name='consultorio-diagnostico-agregar'),

    url(r'^afeccion/(?P<consulta>\d+)/lista$',
        views.AfeccionListView.as_view(),
        name='afecciones-search'),

    url(r'^diagnostico/(?P<consulta>\d+)/(?P<afeccion>\d+)/agregar$',
        views.DiagnosticoRedirectView.as_view(),
        name='diagnostico-agregar'),

    url(r'^profile/persona/(?P<pk>\d+)/editar$',
        views.CliniquePersonaUpdateView.as_view(),
        name='clinique-persona-edit'),

    url(r'^(?P<pk>\d+)/fisico/editar$',
        views.CliniqueFisicoUpdateView.as_view(),
        name='clinique-fisico-editar'),

    url(r'^(?P<pk>\d+)/estilovida/editar$',
        views.CliniqueEstiloVidaUpdateView.as_view(),
        name='clinique-estilovida-editar'),

    url(r'^(?P<pk>\d+)/antecedente/editar$',
        views.CliniqueAntecedenteUpdateView.as_view(),
        name='clinique-antecedente-editar'),

    url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
        views.CliniqueAntecedenteFamiliarUpdateView.as_view(),
        name='clinique-antecedente-familiar-editar'),

    url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
        views.CliniqueAntecedenteQuirurgicoUpdateView.as_view(),
        name='clinique-antecedente-quirurgico-editar'),

    url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
        views.CliniqueAntecedenteObstetricoUpdateView.as_view(),
        name='clinique-antecedente-obstetrico-editar'),

    url(r'^(?P<persona>\d+)/antecedente/obstetrico/agregar',
        views.CliniqueAntecedenteObstetricoCreateView.as_view(),
        name='clinique-antecedente-obstetrico-agregar'),

    url(r'^(?P<consulta>\d+)/ordenmedica/agregar$',
        views.OrdenMedicaCreateView.as_view(),
        name='consultorio-om-agregar'),

    url(r'^paciente/(?P<pk>\d+)/notas$',
        views.PacienteDetailView.as_view(
                template_name='clinique/nota_list.html'),
        name='clinique-notas'),

    url(r'^orden/(?P<pk>\d+)$',
        views.OrdenMedicaDetailView.as_view(),
        name='consultorio-orden-medica'),

    url(r'^orden/(?P<pk>\d+)/impresion$',
        views.OrdenMedicaDetailView.as_view(
                template_name='clinique/ordenmedica_print.html'),
        name='clinique-orden-print'),

    url(r'^orden/(?P<pk>\d+)/completar$',
        views.OrdenCompletarRedirect.as_view(),
        name='clinique-orden-completar'),

    url(r'^consulta/(?P<consulta>\d+)/orden/laboratorio/agregar$',
        views.OrdenLaboratorioCreateView.as_view(),
        name='clinique-orden-laboratorio-agregar'),

    url(r'^consulta/orden/laboratorio/(?P<pk>\d+)$',
        views.OrdenLaboratorioDetailView.as_view(),
        name='clinique-orden-laboratorio'),

    url(r'^consulta/orden/laboratorio/(?P<orden>\d+)/examen/agregar$',
        views.OrdenLaboratorioItemCreateView.as_view(),
        name='clinique-orden-laboratorio-item-agregar'),

    url(r'^consulta/orden/laboratorio/(?P<pk>\d+)/enviar$',
        views.OrdenLaboratorioEnviarView.as_view(),
        name='clinique-orden-laboratorio-enviar'),

    url(r'^consulta/orden/laboratorio/periodo$',
        views.OrdenLaboratorioPeriodoView.as_view(),
        name='clinique-orden-laboratorio-periodo'),

    url(r'^orden/(?P<orden>\d+)/prescripcion/guardar$',
        views.save_prescriptions,
        name='prescripcion-guardar'),

    url(r'^(?P<consulta>\d+)/cargo/agregar$',
        views.CargoCreateView.as_view(),
        name='consultorio-cargo-agregar'),

    url(r'^consulta/(?P<pk>\d+)/emergencia$',
        views.ConsultaEmergenciaRedirectView.as_view(),
        name='consulta-emergencia'),

    url(r'^(?P<consulta>\d+)/nota/medica/agregar$',
        views.NotaMedicaCreateView.as_view(),
        name='nota-medica-agregar'),

    url(r'^(?P<persona>\d+)/(?P<consultorio>\d+)/espera/agregar$',
        views.ConsultorioEsperaCreateView.as_view(),
        name='consultorio-espera-agregar'),

    url(r'^(?P<persona>\d+)/espera/agregar$',
        views.EsperaCreateView.as_view(),
        name='consultorio-espera-u-agregar'),

    url(r'^(?P<pk>\d+)/espera/ausente$',
        views.EsperaAusenteView.as_view(),
        name='clinique-espera-ausente'),

    url(r'^consulta/(?P<pk>\d+)/remitir$',
        views.ConsultaRemitirView.as_view(),
        name='consulta-remitir'),

    url(r'^cita/periodo$',
        views.CitaPeriodoView.as_view(),
        name='cita-periodo'),

    url(r'^espera/periodo$',
        views.EsperaPeriodoView.as_view(),
        name='espera-periodo'),

    url(r'^diagnostico/periodo$',
        views.DiagnosticoPeriodoView.as_view(),
        name='diagnostico-periodo'),

    url(r'^cargo/periodo$',
        views.CargoPeriodoView.as_view(),
        name='cargo-periodo'),

    url(r'^evaluacion/periodo$',
        views.EvaluacionPeriodoView.as_view(),
        name='evaluacion-periodo'),

    url(r'^ordenes/periodo$',
        views.OrdenMedicaPeriodoListView.as_view(),
        name='orden-periodo'),

    url(r'^seguimiento/periodo$',
        views.SeguimientoPeriodoView.as_view(),
        name='seguimiento-periodo'),

    url(r'^(?P<persona>\d+)/(?P<consulta>\d+)/prescripcion/agregar$',
        views.PrescripcionCreateView.as_view(),
        name='consultorio-prescripcion-agregar'),

    url(r'^prescripcion/(?P<pk>\d+)/editar$',
        views.PrescripcionUpdateView.as_view(),
        name='clinique-prescripcion-edit'),

    url(r'^(?P<persona>\d+)/(?P<consulta>\d+)/incapacidad/agregar$',
        views.IncapacidadCreateView.as_view(),
        name='consultorio-incapacidad-agregar'),

    url(r'^incapacidad/(?P<pk>\d+)/editar$',
        views.IncapacidadUpdateView.as_view(),
        name='clinique-incapacidad-edit'),

    url(r'^incapacidad/list$',
        views.IncapacidadListView.as_view(),
        name='clinique-incapacidad-list'),

    url(r'^(?P<persona>\d+)/remision/agregar$',
        views.RemisionCreateView.as_view(),
        name='consultorio-remision-agregar'),

    url(r'^(?P<persona>\d+)/historia/fisica/(?P<espera>\d+)/agregar$',
        views.HistoriaFisicaEsperaCreateView.as_view(),
        name='persona-historia-agregar-espera'),
]
