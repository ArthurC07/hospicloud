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

from nightingale import views

urlpatterns = [

    url(r'^$',
        views.NightingaleIndexView.as_view(),
        name='nightingale-index'),

    url(r'^(?P<pk>\d+)$',
        views.NightingaleDetailView.as_view(),
        name='nightingale-view-id'),

    url(r'^admisiones$',
        views.CargoDeleteView.as_view(),
        name='enfermeria-admisiones'),

    url(r'^(?P<pk>\d+)/resumen$',
        views.ResumenDetailView.as_view(),
        name='nightingale-resume'),

    url(r'^(?P<pk>\d+)/devoluciones$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/devoluciones.html'),
        name='enfermeria-devoluciones'),

    url(r'^(?P<pk>\d+)/signos/grafico$',
        views.SignosDetailView.as_view(),
        name='nightingale-signos-grafico'),

    url(r'^(?P<pk>\d+)/cargos$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/cargos.html'),
        name='enfermeria-cargos'),

    url(r'^(?P<admision>\d+)/cargo/agregar$',
        views.CargoCreateView.as_view(),
        name='enfermeria-cargo-agregar'),

    url(r'^(?P<admision>\d+)/cargo/(?P<item>\d+)/agregar$',
        views.ChosenCargoCreateView.as_view(),
        name='enfermeria-cargo-pre-agregar'),

    url(r'^cargo/(?P<pk>\d+)/eliminar$',
        views.CargoDeleteView.as_view(),
        name='enfermeria-cargo-eliminar'),

    url(r'^cargo/(?P<pk>\d+)/editar',
        views.CargoUpdateView.as_view(),
        name='enfermeria-cargo-editar'),

    url(r'^(?P<pk>\d+)/signos$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/signos.html'),
        name='enfermeria-signos'),

    url(r'^(?P<admision>\d+)/signo/agregar$',
        views.SignoVitalCreateView.as_view(),
        name='enfermeria-signo-agregar'),

    url(r'^(?P<pk>\d+)/ordenes$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/ordenes.html'),
        name='enfermeria-ordenes'),

    url(r'^nota/(?P<pk>\d+)/editar$',
        views.NotaUpdateView.as_view(),
        name='enfermeria-nota-editar'),

    url(r'^(?P<admision>\d+)/orden/agregar$',
        views.OrdenCreateView.as_view(),
        name='enfermeria-orden-agregar'),

    url(r'^(?P<pk>\d+)/evolucion$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/evolucion.html'),
        name='enfermeria-evolucion'),

    url(r'^(?P<admision>\d+)/evolucion/agregar$',
        views.EvolucionCreateView.as_view(),
        name='enfermeria-evolucion-agregar'),

    url(r'^(?P<pk>\d+)/ie$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/ie.html'),
        name='enfermeria-ingestas-excretas'),

    url(r'^(?P<admision>\d+)/ingesta/agregar$',
        views.IngestaCreateView.as_view(),
        name='enfermeria-ingesta-agregar'),

    url(r'^(?P<admision>\d+)/excreta/agregar$',
        views.ExcretaCreateView.as_view(),
        name='enfermeria-excreta-agregar'),

    url(r'^(?P<pk>\d+)/glucometria$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/glucometria.html'),
        name='enfermeria-glucometria'),

    url(r'^(?P<admision>\d+)/glicemia/agregar$',
        views.GlicemiaCreateView.as_view(),
        name='enfermeria-glicemia-agregar'),

    url(r'^(?P<admision>\d+)/insulina/agregar$',
        views.InsulinaCreateView.as_view(),
        name='enfermeria-insulina-agregar'),

    url(r'^(?P<admision>\d+)/glucosuria/agregar$',
        views.GlucosuriaCreateView.as_view(),
        name='enfermeria-glucosuria-agregar'),

    url(r'^(?P<admision>\d+)/devolucion/agregar$',
        views.DevolucionCreateView.as_view(),
        name='enfermeria-devolucion-agregar'),

    url(r'^(?P<pk>\d+)/notas$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/notas.html'),
        name='enfermeria-notas'),

    url(r'^(?P<admision>\d+)/nota/agregar$',
        views.NotaCreateView.as_view(),
        name='enfermeria-nota-agregar'),

    url(r'^(?P<pk>\d+)/medicamentos$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/medicamentos.html'),
        name='enfermeria-medicamentos'),

    url(r'^(?P<pk>\d+)/cuenta$',
        views.NightingaleDetailView.as_view(
                template_name='enfermeria/cuenta.html'),
        name='enfermeria-cuenta'),

    url(r'^(?P<admision>\d+)/medicamento/agregar$',
        views.MedicamentoCreateView.as_view(),
        name='enfermeria-medicamento-agregar'),

    url(r'^medicamento/(?P<pk>\d+)/(?P<estado>\d+)/suspender$',
        views.MedicamentoSuspenderView.as_view(),
        name='enfermeria-medicamento-suspender'),

    url(r'^nota/(?P<pk>\d+)/cerrar$',
        views.NotaCerrarView.as_view(),
        name='enfermeria-nota-cerrar'),

    url(r'^(?P<medicamento>\d+)/dosis/agregar$',
        views.DosisCreateView.as_view(),
        name='enfermeria-dosis-agregar'),

    url(r'^dosis/(?P<pk>\d+)/(?P<estado>\d+)/suministrar$',
        views.DosisSuministrarView.as_view(),
        name='enfermeria-dosis-suministrar'),

    url(r'^(?P<admision>\d+)/alta',
        views.SumarioCreateView.as_view(),
        name='enfermeria-dar-alta'),

    url(r'^(?P<medicamento>\d+)/dosificar',
        views.DosificarMedicamentoView.as_view(),
        name='enfermeria-dosificar-medicamento'),

    url(r'^(?P<pk>\d+)/editar',
        views.MedicamentoUpdateView.as_view(),
        name='enfermeria-editar-medicamento'),

    url(r'^(?P<pk>\d+)/oxigeno$',
        views.NightingaleDetailView.as_view(
                template_name='nightingale/oxigeno.html'),
        name='enfermeria-oxigeno'),

    url(r'^(?P<admision>\d+)/oxigeno/iniciar$',
        views.OxigenoTerapiaCreateView.as_view(),
        name='enfermeria-oxigeno-iniciar'),

    url(r'^(?P<pk>\d+)/oxigeno/terminar$',
        views.OxigenoTerapiaUpdateView.as_view(),
        name='enfermeria-oxigeno-terminar'),

    url(r'^(?P<pk>\d+)/honorarios$',
        views.NightingaleDetailView.as_view(
                template_name='nightingale/honorarios.html'),
        name='enfermeria-honorarios'),

    url(r'^(?P<admision>\d+)/honorario/agregar$',
        views.HonorarioCreateView.as_view(),
        name='enfermeria-honorario-agregar'),

    url(r'^(?P<pk>\d+)/honorario/editar$',
        views.HonorarioUpdateView.as_view(),
        name='enfermeria-honorario-editar'),

    url(r'^(?P<pk>\d+)/honorario/eliminar$',
        views.HonorarioDeleteView.as_view(),
        name='enfermeria-honorario-eliminar'),
]
