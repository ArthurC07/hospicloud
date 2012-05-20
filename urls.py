# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import IndexView, CustomSearchView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tastypie.api import Api
admin.autodiscover()
from persona.api import PersonaResource

v1_api = Api(api_name='mobile')
v1_api.register(PersonaResource())

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^persona/', include('hospinet.persona.urls')),
    url(r'^examen/', include('hospinet.laboratory.urls')),
    url(r'^accounts/', include('hospinet.users.urls')),
    url(r'^admision/', include('hospinet.spital.urls')),
    url(r'^reportes/', include('hospinet.statistics.urls')),
    url(r'^enfermeria/', include('hospinet.nightingale.urls')),
    url(r'^consultorio/', include('hospinet.clinique.urls')),
    url(r'^busqueda/', CustomSearchView(), name='haystack_search'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^private_files/', include('private_files.urls')),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
