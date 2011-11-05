# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$',
        ExamenDetailView.as_view(),
        name='examen-view-id'),
)
