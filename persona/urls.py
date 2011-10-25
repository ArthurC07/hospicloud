# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from persona.views import (PersonaDetailView, PersonaCreateView,
    PersonaUpdateView, EstiloVidaUpdateView, AntecedenteUpdateView,
    AntecedenteFamiliarUpdateView, AntecedenteObstetricoUpdateView)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$',
        PersonaDetailView.as_view(),
        name='persona-view-id'),
    
    url(r'^nuevo$',
        PersonaCreateView.as_view(),
        name='persona-create'),
    
    url(r'^(?P<pk>\d+)/editar$',
        PersonaUpdateView.as_view(),
        name='persona-editar'),
    
    url(r'^(?P<pk>\d+)/estilovida/editar$',
        EstiloVidaUpdateView.as_view(),
        name='persona-estilovida-editar'),
    
    url(r'^(?P<pk>\d+)/antecedente/editar$',
        AntecedenteUpdateView.as_view(),
        name='persona-antecedente-editar'),
    
    url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
        AntecedenteFamiliarUpdateView.as_view(),
        name='persona-antecedente-familiar-editar'),
    
    url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
        AntecedenteObstetricoUpdateView.as_view(),
        name='persona-antecedente-obstetrico-editar'),
)
