# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from nightingale.views import (NightingaleIndexView, NightingaleDetailView,
    IngresarView, CargoCreateView)

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
    
    url(r'^(?P<pk>\d+)/cargos$',
        NightingaleDetailView.as_view(template_name='enfermeria/cargos.djhtml'),
        name='enfermeria-cargos'),
    
    url(r'^(?P<admision>\d+)/cargo/agregar$',
        CargoCreateView.as_view(),
        name='enfermeria-cargo-agregar'),
    
    url(r'^(?P<pk>\d+)/signos$',
        NightingaleDetailView.as_view(),
        name='enfermeria-signos'),
    
    url(r'^(?P<pk>\d+)/ordenes$',
        NightingaleDetailView.as_view(),
        name='enfermeria-ordenes'),
    
    url(r'^(?P<pk>\d+)/evolucion$',
        NightingaleDetailView.as_view(),
        name='enfermeria-evolucion'),
    
    url(r'^(?P<pk>\d+)/ingestas$',
        NightingaleDetailView.as_view(),
        name='enfermeria-ingestas-excretas'),
    
    url(r'^(?P<pk>\d+)/glucometria$',
        NightingaleDetailView.as_view(),
        name='enfermeria-glucometria'),
    
    url(r'^(?P<pk>\d+)/notas$',
        NightingaleDetailView.as_view(),
        name='enfermeria-notas'),
)
