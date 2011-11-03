# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import IndexView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^persona/', include('hospinet.persona.urls')),
    url(r'^accounts/', include('hospinet.users.urls')),
)

urlpatterns += staticfiles_urlpatterns()
