# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from statistics.views import (AtencionAdulto, Estadisticas, AtencionInfantil)

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
)
