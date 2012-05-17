# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from clinique.views import ConsultorioDetailView, ConsultorioIndex

urlpatterns = patterns('',
     url(r'^$',
        ConsultorioIndex.as_view(),
        name='consultorio-index'),
    
    url(r'^(?P<pk>\d+)$',
        ConsultorioDetailView.as_view(),
        name='consultorio-view'),
    
    url(r'^(?P<pk>\d+)/pacientes$',
        ConsultorioDetailView.as_view(template_name='consultorio/pacientes_detail.djhtml'),
        name='consultorio-pacientes'),
)
