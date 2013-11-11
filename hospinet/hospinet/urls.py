# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2013 Carlos Flores <cafg10@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from hospinet.views import IndexView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from tastypie.api import Api
admin.autodiscover()
from persona.api import PersonaResource
from nightingale.api import MedicamentoResource
from inventory.api import ItemTemplateResource
from spital.api import AdmisionResource, HabitacionResource

v1_api = Api(api_name='mobile')
v1_api.register(PersonaResource())
v1_api.register(MedicamentoResource())
v1_api.register(ItemTemplateResource())
v1_api.register(AdmisionResource())
v1_api.register(HabitacionResource())

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^persona/', include('persona.urls')),
    url(r'^examen/', include('imaging.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^admision/', include('spital.urls')),
    url(r'^reportes/', include('statistics.urls')),
    url(r'^enfermeria/', include('nightingale.urls')),
    url(r'^consultorio/', include('clinique.urls')),
    url(r'^caja/', include('invoice.urls')),
    url(r'^emergencia/', include('emergency.urls')),
    url(r'^bussiness/', include('statistics.urls')),
    url(r'^api/', include(v1_api.urls)),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

