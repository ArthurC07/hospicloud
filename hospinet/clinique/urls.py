# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from clinique.views import (ConsultorioIndex, ConsultorioDetailView,
    PacienteCreateView, PacientePreCreateView, ConsultorioCreateView,
    SecretariaCreateView, PersonaConsultorioCreateView, PacienteDetailView,
    EsperaPacientes, EsperadorAgregarView, EsperadorAtendido, RecetaCreateView,
    RecetaDetailView, ConsultaCreateView,
    OptometriaCreateView, OptometriaDetailView, HistoriaClinicaCreateView)

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
        ConsultorioDetailView.as_view(template_name='consultorio/paciente_list.html'),
        name='consultorio-pacientes'),
    
    url(r'^(?P<consultorio>\d+)/espera$',
        EsperaPacientes.as_view(),
        name='consultorio-espera'),
    
    url(r'^(?P<consultorio>\d+)/secretaria/agregar$',
        SecretariaCreateView.as_view(),
        name='consultorio-secretaria-agregar'),
    
    url(r'^paciente/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(),
        name='consultorio-paciente'),
    
    url(r'^optometrias/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(template_name='consultorio/optometrias.html'),
        name='consultorio-paciente-optometrias'),
    
    url(r'^consultas/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(template_name='consultorio/consultas.html'),
        name='consultorio-paciente-consultas'),
    
    url(r'^historia/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(template_name='consultorio/historia.html'),
        name='consultorio-paciente-historia'),
    
    url(r'^recetas/(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        PacienteDetailView.as_view(template_name='consultorio/recetas.html'),
        name='consultorio-paciente-recetas'),
    
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
    
    url(r'^(?P<paciente>\d+)/esperador/nuevo$',
        EsperadorAgregarView.as_view(),
        name='consultorio-esperador-nuevo'),
    
    url(r'^paciente/(?P<esperador>\d+)/atender$',
        EsperadorAtendido.as_view(),
        name='consultorio-esperador-atender'),
    
    url(r'^(?P<paciente>\d+)/consulta/nueva$',
        ConsultaCreateView.as_view(),
        name='consultorio-consulta-nueva'),
    
    url(r'^receta/(?P<pk>\d+)$',
        ConsultorioDetailView.as_view(),
        name='consultorio-consulta-view'),
    
    url(r'^(?P<paciente>\d+)/historia/nueva$',
        HistoriaClinicaCreateView.as_view(),
        name='consultorio-historia-nueva'),
    
    url(r'^(?P<paciente>\d+)/receta/nueva$',
        RecetaCreateView.as_view(),
        name='consultorio-receta-nueva'),
    
    url(r'^receta/(?P<pk>\d+)$',
        RecetaDetailView.as_view(),
        name='consultorio-receta-view'),
    
    url(r'^(?P<paciente>\d+)/optometria/nueva$',
        OptometriaCreateView.as_view(),
        name='consultorio-optometria-nueva'),
    
    url(r'^optometria/(?P<pk>\d+)$',
        OptometriaDetailView.as_view(),
        name='consultorio-optometria-view'),
)
