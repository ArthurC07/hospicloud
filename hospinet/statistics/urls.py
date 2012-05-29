# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from statistics.views import (AtencionAdulto, Estadisticas, AtencionInfantil,
    Productividad, IngresosHospitalarios)

urlpatterns = patterns('',
    
    url(r'^$',
        Estadisticas.as_view(),
        name='estadisticas'),
    
    url(r'^estadisticas/adulto$',
        AtencionAdulto.as_view(),
        name='estadisticas-admision-adulto'),
    
    url(r'^estadisticas/infantil$',
        AtencionInfantil.as_view(),
        name='estadisticas-admision-infantil'),
    
    url(r'^estadisticas/productividad$',
        Productividad.as_view(),
        name='estadisticas-productividad'),
    
    url(r'^estadisticas/ingresos$',
        IngresosHospitalarios.as_view(),
        name='estadisticas-ingresos-hospitalarios'),
)
