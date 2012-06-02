# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from clinique.views import (ConsultorioDetailView, ConsultorioIndex,
    PacienteCreateView, PacientePreCreateView, ConsultorioCreateView,
    SecretariaCreateView, PersonaConsultorioCreateView, PacienteDetailView)

urlpatterns = patterns('',
     url(r'^$',
        ConsultorioIndex.as_view(),
        name='consultorio-index'),
     
     url(r'^agregar$',
        ConsultorioCreateView.as_view(),
        name='consultorio-agregar'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        ConsultorioDetailView.as_view(),
        name='consultorio-view'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/citas$',
        ConsultorioDetailView.as_view(template_name='consultorio/citas.html'),
        name='consultorio-citas'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/pacientes$',
        ConsultorioDetailView.as_view(template_name='consultorio/pacientes_detail.html'),
        name='consultorio-pacientes'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})/espera$',
        ConsultorioDetailView.as_view(template_name='consultorio/espera.html'),
        name='consultorio-espera'),
    
    url(r'^(?P<consultorio>\d+)/secretaria/agregar$',
        SecretariaCreateView.as_view(),
        name='consultorio-secretaria-agregar'),
    
    url(r'^paciente/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(),
        name='consultorio-paciente'),
    
    url(r'^(?P<consultorio>\d+)/paciente/nuevo$',
        PacientePreCreateView.as_view(),
        name='consultorio-paciente-nuevo'),
    
    url(r'^(?P<consultorio>\d+)/persona/nueva$',
        PersonaConsultorioCreateView.as_view(),
        name='consultorio-persona-nueva'),
	
	url(r'^(?P<consultorio>\d+)/paciente/(?P<persona>\d+)/agregar$',
        PacienteCreateView.as_view(),
        name='consultorio-paciente-agregar'),
    
    url(r'^(?P<consultorio>\d+)/cita/nueva$',
        PacientePreCreateView.as_view(),
        name='consultorio-cita-nueva'),
    
    url(r'^(?P<consultorio>\d+)/esperador/nuevo$',
        PacientePreCreateView.as_view(),
        name='consultorio-esperador-nuevo'),
	
)
