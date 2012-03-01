# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from spital.views import (AdmisionIndexView, PersonaAdmisionCreateView,
    AdmisionCreateView, IngresarView, AdmisionDetailView, AutorizarView,
    FiadorAgregarView, ReferenciaAgregarView, PersonaFiadorCreateView,
    PersonaReferenciaCreateView, HospitalizarView, PagarView, AtencionAdulto,
    Estadisticas)

urlpatterns = patterns('',
    
    url(r'^$',
        AdmisionIndexView.as_view(),
        name='admision-index'),
    
    url(r'^(?P<pk>\d+)$',
        AdmisionDetailView.as_view(),
        name='admision-view-id'),
    
    url(r'^(?P<slug>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$',
        AdmisionDetailView.as_view(),
        name='admision-view-slug'),
    
    url(r'^(?P<pk>\d+)/autorizacion$',
        AdmisionDetailView.as_view(template_name="admision/autorizacion.djhtml"),
        name='admision-autorizacion'),
    
    url(r'^(?P<pk>\d+)/fiadores$',
        AdmisionDetailView.as_view(template_name="admision/admision_fiadores.djhtml"),
        name='admision-fiadores'),
    
    url(r'^(?P<admision>\d+)/fiadores/agregar$',
        PersonaFiadorCreateView.as_view(),
        name='admision-fiador'),
    
    url(r'^(?P<admision>\d+)/fiadores/agregar/(?P<persona>\d+)$',
        FiadorAgregarView.as_view(),
        name='admision-fiador-agregar'),
    
    url(r'^(?P<pk>\d+)/referencias$',
        AdmisionDetailView.as_view(template_name="admision/admision_referencias.djhtml"),
        name='admision-referencias'),
    
    url(r'^(?P<admision>\d+)/referencias/agregar$',
        PersonaReferenciaCreateView.as_view(),
        name='admision-referencia'),
    
    url(r'^(?P<admision>\d+)/referencias/agregar/(?P<persona>\d+)$',
        ReferenciaAgregarView.as_view(),
        name='admision-referencia-agregar'),
    
    url(r'^(?P<pk>\d+)/autorizar$',
        AutorizarView.as_view(),
        name='admision-autorizar'),
    
    url(r'^(?P<pk>\d+)/hospitalizar$',
        HospitalizarView.as_view(),
        name='admision-hospitalizar'),
    
    url(r'^(?P<pk>\d+)/pagar$',
        PagarView.as_view(),
        name='admision-pagar'),
    
    url(r'^ingresar$',
        IngresarView.as_view(),
        name='admision-iniciar'),
    
    url(r'^persona/ingresar$',
        PersonaAdmisionCreateView.as_view(),
        name='admision-ingresar-persona'),
    
    url(r'^estadisticas$',
        Estadisticas.as_view(),
        name='admision-estadisticas'),
    
    url(r'^estadisticas/adulto$',
        AtencionAdulto.as_view(),
        name='admision-estadisticas-adulto'),
    
    url(r'^persona/(?P<persona>\d+)$',
        AdmisionCreateView.as_view(),
        name='admision-persona-agregar'),
)
