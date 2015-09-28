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

from nightingale.views import (NightingaleIndexView, NightingaleDetailView,
                               CargoCreateView, EvolucionCreateView,
                               GlicemiaCreateView,
                               InsulinaCreateView, GlucosuriaCreateView,
                               IngestaCreateView, OrdenCreateView,
                               NotaCreateView, SignoVitalCreateView,
                               SignosDetailView, ExcretaCreateView,
                               MedicamentoCreateView, DosisSuministrarView,
                               NotaUpdateView, ResumenDetailView,
                               DosisCreateView,
                               MedicamentoSuspenderView,
                               DevolucionCreateView, NotaCerrarView,
                               SumarioCreateView, CargoDeleteView,
                               DosificarMedicamentoView,
                               MedicamentoUpdateView, OxigenoTerapiaCreateView,
                               OxigenoTerapiaUpdateView, HonorarioCreateView,
                               HonorarioUpdateView, ChosenCargoCreateView,
                               HonorarioDeleteView, CargoUpdateView)


urlpatterns = patterns('',

                       url(r'^$',
                           NightingaleIndexView.as_view(),
                           name='nightingale-index'),

                       url(r'^(?P<pk>\d+)$',
                           NightingaleDetailView.as_view(),
                           name='nightingale-view-id'),

                       url(r'^admisiones$',
                           CargoDeleteView.as_view(),
                           name='enfermeria-admisiones'),

                       url(
                           r'^(?P<pk>\d+)/resumen$',
                           ResumenDetailView.as_view(),
                           name='nightingale-resume'),

                       url(
                           r'^(?P<pk>\d+)/devoluciones$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/devoluciones.html'),
                           name='enfermeria-devoluciones'),

                       url(r'^(?P<pk>\d+)/signos/grafico$',
                           SignosDetailView.as_view(),
                           name='nightingale-signos-grafico'),

                       url(r'^(?P<pk>\d+)/cargos$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/cargos.html'),
                           name='enfermeria-cargos'),

                       url(r'^(?P<admision>\d+)/cargo/agregar$',
                           CargoCreateView.as_view(),
                           name='enfermeria-cargo-agregar'),

                       url(r'^(?P<admision>\d+)/cargo/(?P<item>\d+)/agregar$',
                           ChosenCargoCreateView.as_view(),
                           name='enfermeria-cargo-pre-agregar'),

                       url(r'^cargo/(?P<pk>\d+)/eliminar$',
                           CargoDeleteView.as_view(),
                           name='enfermeria-cargo-eliminar'),

                       url(r'^cargo/(?P<pk>\d+)/editar',
                           CargoUpdateView.as_view(),
                           name='enfermeria-cargo-editar'),

                       url(r'^(?P<pk>\d+)/signos$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/signos.html'),
                           name='enfermeria-signos'),

                       url(r'^(?P<admision>\d+)/signo/agregar$',
                           SignoVitalCreateView.as_view(),
                           name='enfermeria-signo-agregar'),

                       url(r'^(?P<pk>\d+)/ordenes$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/ordenes.html'),
                           name='enfermeria-ordenes'),
                       url(r'^nota/(?P<pk>\d+)/editar$',
                           NotaUpdateView.as_view(),
                           name='enfermeria-nota-editar'),

                       url(r'^(?P<admision>\d+)/orden/agregar$',
                           OrdenCreateView.as_view(),
                           name='enfermeria-orden-agregar'),

                       url(r'^(?P<pk>\d+)/evolucion$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/evolucion.html'),
                           name='enfermeria-evolucion'),

                       url(r'^(?P<admision>\d+)/evolucion/agregar$',
                           EvolucionCreateView.as_view(),
                           name='enfermeria-evolucion-agregar'),

                       url(r'^(?P<pk>\d+)/ie$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/ie.html'),
                           name='enfermeria-ingestas-excretas'),

                       url(r'^(?P<admision>\d+)/ingesta/agregar$',
                           IngestaCreateView.as_view(),
                           name='enfermeria-ingesta-agregar'),

                       url(r'^(?P<admision>\d+)/excreta/agregar$',
                           ExcretaCreateView.as_view(),
                           name='enfermeria-excreta-agregar'),

                       url(r'^(?P<pk>\d+)/glucometria$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/glucometria.html'),
                           name='enfermeria-glucometria'),

                       url(r'^(?P<admision>\d+)/glicemia/agregar$',
                           GlicemiaCreateView.as_view(),
                           name='enfermeria-glicemia-agregar'),

                       url(r'^(?P<admision>\d+)/insulina/agregar$',
                           InsulinaCreateView.as_view(),
                           name='enfermeria-insulina-agregar'),

                       url(r'^(?P<admision>\d+)/glucosuria/agregar$',
                           GlucosuriaCreateView.as_view(),
                           name='enfermeria-glucosuria-agregar'),

                       url(r'^(?P<admision>\d+)/devolucion/agregar$',
                           DevolucionCreateView.as_view(),
                           name='enfermeria-devolucion-agregar'),

                       url(r'^(?P<pk>\d+)/notas$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/notas.html'),
                           name='enfermeria-notas'),

                       url(r'^(?P<admision>\d+)/nota/agregar$',
                           NotaCreateView.as_view(),
                           name='enfermeria-nota-agregar'),

                       url(r'^(?P<pk>\d+)/medicamentos$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/medicamentos.html'),
                           name='enfermeria-medicamentos'),

                       url(r'^(?P<pk>\d+)/cuenta$',
                           NightingaleDetailView.as_view(
                               template_name='enfermeria/cuenta.html'),
                           name='enfermeria-cuenta'),

                       url(r'^(?P<admision>\d+)/medicamento/agregar$',
                           MedicamentoCreateView.as_view(),
                           name='enfermeria-medicamento-agregar'),

                       url(
                           r'^medicamento/(?P<pk>\d+)/(?P<estado>\d+)/suspender$',
                           MedicamentoSuspenderView.as_view(),
                           name='enfermeria-medicamento-suspender'),

                       url(r'^nota/(?P<pk>\d+)/cerrar$',
                           NotaCerrarView.as_view(),
                           name='enfermeria-nota-cerrar'),

                       url(r'^(?P<medicamento>\d+)/dosis/agregar$',
                           DosisCreateView.as_view(),
                           name='enfermeria-dosis-agregar'),

                       url(r'^dosis/(?P<pk>\d+)/(?P<estado>\d+)/suministrar$',
                           DosisSuministrarView.as_view(),
                           name='enfermeria-dosis-suministrar'),

                       url(r'^(?P<admision>\d+)/alta',
                           SumarioCreateView.as_view(),
                           name='enfermeria-dar-alta'),

                       url(r'^(?P<medicamento>\d+)/dosificar',
                           DosificarMedicamentoView.as_view(),
                           name='enfermeria-dosificar-medicamento'),

                       url(r'^(?P<pk>\d+)/editar',
                           MedicamentoUpdateView.as_view(),
                           name='enfermeria-editar-medicamento'),

                       url(r'^(?P<pk>\d+)/oxigeno$',
                           NightingaleDetailView.as_view(
                               template_name='nightingale/oxigeno.html'),
                           name='enfermeria-oxigeno'),

                       url(r'^(?P<admision>\d+)/oxigeno/iniciar$',
                           OxigenoTerapiaCreateView.as_view(),
                           name='enfermeria-oxigeno-iniciar'),

                       url(r'^(?P<pk>\d+)/oxigeno/terminar$',
                           OxigenoTerapiaUpdateView.as_view(),
                           name='enfermeria-oxigeno-terminar'),

                       url(r'^(?P<pk>\d+)/honorarios$',
                           NightingaleDetailView.as_view(
                               template_name='nightingale/honorarios.html'),
                           name='enfermeria-honorarios'),

                       url(r'^(?P<admision>\d+)/honorario/agregar$',
                           HonorarioCreateView.as_view(),
                           name='enfermeria-honorario-agregar'),

                       url(r'^(?P<pk>\d+)/honorario/editar$',
                           HonorarioUpdateView.as_view(),
                           name='enfermeria-honorario-editar'),

                       url(r'^(?P<pk>\d+)/honorario/eliminar$',
                           HonorarioDeleteView.as_view(),
                           name='enfermeria-honorario-eliminar'),
)
