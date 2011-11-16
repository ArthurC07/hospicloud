# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from persona.views import (PersonaDetailView, PersonaCreateView,
    PersonaUpdateView, EstiloVidaUpdateView, AntecedenteUpdateView,
    AntecedenteFamiliarUpdateView, AntecedenteObstetricoUpdateView,
    PersonaIndexView, FisicoUpdateView)

urlpatterns = patterns('',
    
    url(r'^$',
        PersonaIndexView.as_view(),
        name='persona-index'),
    
    url(r'^(?P<pk>\d+)$',
        PersonaDetailView.as_view(),
        name='persona-view-id'),
    
    url(r'^(?P<pk>\d+)/estilovida$',
        PersonaDetailView.as_view(template_name='persona/estilo_detail.djhtml'),
        name='persona-estilo'),
    
    url(r'^agregar$',
        PersonaCreateView.as_view(),
        name='persona-create'),
    
    url(r'^(?P<pk>\d+)/editar$',
        PersonaUpdateView.as_view(),
        name='persona-editar'),
    
    url(r'^(?P<pk>\d+)/fisico/editar$',
        FisicoUpdateView.as_view(),
        name='persona-fisico-editar'),
    
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
