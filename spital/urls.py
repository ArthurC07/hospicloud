# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from spital.views import (AdmisionIndexView, PersonaAdmisionCreateView,
    AdmisionCreateView, IngresarView, AdmisionDetailView)

urlpatterns = patterns('',
    
    url(r'^$',
        AdmisionIndexView.as_view(),
        name='admision-index'),
    
    url(r'^(?P<pk>\d+)$',
        AdmisionDetailView.as_view(),
        name='admision-view-id'),
    
    url(r'^ingresar$',
        IngresarView.as_view(),
        name='admision-iniciar'),
    
    url(r'^persona/ingresar$',
        PersonaAdmisionCreateView.as_view(),
        name='admision-ingresar-persona'),
    
    url(r'^persona/(?P<persona>\d+)$',
        AdmisionCreateView.as_view(),
        name='admision-persona-agregar'),
)
