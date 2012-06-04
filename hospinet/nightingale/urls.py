# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from nightingale.views import (NightingaleIndexView, NightingaleDetailView,
    IngresarView, CargoCreateView, EvolucionCreateView, GlicemiaCreateView,
    InsulinaCreateView, GlucosuriaCreateView, IngestaCreateView,
    NotaCreateView, SignoVitalCreateView, SignosDetailView, ExcretaCreateView, 
    MedicamentoCreateView, DosisSuministrarView)

urlpatterns = patterns('',
    
    url(r'^$',
        NightingaleIndexView.as_view(),
        name='nightingale-index'),
    
    url(r'^(?P<pk>\d+)/ingresar',
        IngresarView.as_view(),
        name='enfermeria-ingresar'),
    
    url(r'^(?P<pk>\d+)$',
        NightingaleDetailView.as_view(),
        name='nightingale-view-id'),
    
    url(r'^(?P<pk>\d+)/signos/grafico$',
        SignosDetailView.as_view(),
        name='nightingale-signos-grafico'),
    
    url(r'^(?P<pk>\d+)/cargos$',
        NightingaleDetailView.as_view(template_name='enfermeria/cargos.html'),
        name='enfermeria-cargos'),
    
    url(r'^(?P<admision>\d+)/cargo/agregar$',
        CargoCreateView.as_view(),
        name='enfermeria-cargo-agregar'),
    
    url(r'^(?P<pk>\d+)/signos$',
        NightingaleDetailView.as_view(template_name='enfermeria/signos.html'),
        name='enfermeria-signos'),
    
    url(r'^(?P<admision>\d+)/signo/agregar$',
        SignoVitalCreateView.as_view(),
        name='enfermeria-signo-agregar'),
    
    url(r'^(?P<pk>\d+)/ordenes$',
        NightingaleDetailView.as_view(template_name='enfermeria/ordenes.html'),
        name='enfermeria-ordenes'),
    
    url(r'^(?P<admision>\d+)/orden/agregar$',
        NotaCreateView.as_view(),
        name='enfermeria-orden-agregar'),
    
    url(r'^(?P<pk>\d+)/evolucion$',
        NightingaleDetailView.as_view(template_name='enfermeria/evolucion.html'),
        name='enfermeria-evolucion'),
    
    url(r'^(?P<admision>\d+)/evolucion/agregar$',
        EvolucionCreateView.as_view(),
        name='enfermeria-evolucion-agregar'),
    
    url(r'^(?P<pk>\d+)/ie$',
        NightingaleDetailView.as_view(template_name='enfermeria/ie.html'),
        name='enfermeria-ingestas-excretas'),
    
    url(r'^(?P<admision>\d+)/ingesta/agregar$',
        IngestaCreateView.as_view(),
        name='enfermeria-ingesta-agregar'),
    
    url(r'^(?P<admision>\d+)/ingesta/agregar$',
        ExcretaCreateView.as_view(),
        name='enfermeria-excreta-agregar'),
    
    url(r'^(?P<pk>\d+)/glucometria$',
        NightingaleDetailView.as_view(template_name='enfermeria/glucometria.html'),
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
    
    url(r'^(?P<pk>\d+)/notas$',
        NightingaleDetailView.as_view(template_name='enfermeria/notas.html'),
        name='enfermeria-notas'),
    
    url(r'^(?P<admision>\d+)/nota/agregar$',
        NotaCreateView.as_view(),
        name='enfermeria-nota-agregar'),
    
    url(r'^(?P<pk>\d+)/medicamentos$',
        NightingaleDetailView.as_view(template_name='enfermeria/medicamentos.html'),
        name='enfermeria-medicamentos'),

    url(r'^(?P<admision>\d+)/medicamento/agregar$',
        MedicamentoCreateView.as_view(),
        name='enfermeria-medicamento-agregar'),
    
    url(r'^dosis/(?P<pk>\d+)/suministrar$',
        DosisSuministrarView.as_view(),
        name='enfermeria-dosis-suministrar'),
)
