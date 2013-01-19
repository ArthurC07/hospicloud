# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from invoice.views import (IndexView, ReciboPersonaCreateView, ReciboDetailView,
                           VentaCreateView, ReporteView)

urlpatterns = patterns('',
    
    url(r'^$',
        IndexView.as_view(),
        name='invoice-index'),

    url(r'^(?P<persona>\d+)/crear',
        ReciboPersonaCreateView.as_view(),
        name='invoice-create'),
    
    url(r'^(?P<pk>\d+)$',
        ReciboDetailView.as_view(),
        name='invoice-view-id'),
    
    url(r'^(?P<recibo>\d+)/venta/add$',
        VentaCreateView.as_view(),
        name='venta-add'),

    url(r'^periodo$',
        ReporteView.as_view(),
        name='invoice-periodo'),

)
