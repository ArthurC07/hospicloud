# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from laboratory.views import (ExamenDetailView, ExamenCreateView,
    ExamenUpdateView, ImagenCreateView)

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$',
        ExamenDetailView.as_view(),
        name='examen-view-id'),
    
    url(r'^(?P<persona>\d+)$/nuevo',
        ExamenCreateView.as_view(),
        name='examen-create'),
    
    url(r'^(?P<pk>\d+)/editar$',
        ExamenUpdateView.as_view(),
        name='examen-editar'),
    
    url(r'^(?P<examen>\d+)/imagen/agregar$',
        ImagenCreateView.as_view(),
        name='examen-imagen-agregar'),
)
