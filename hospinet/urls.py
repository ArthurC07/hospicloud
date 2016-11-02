# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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
from django.conf.urls import include, url
from django.conf.urls.static import static
from userena.views import profile_edit
from hospinet import views

from hospinet.views import IndexView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from users.forms import CustomEditProfileForm

admin.autodiscover()

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin
    # documentation:
    # url(r'^admin/doc/', include(
    # 'django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^persona/', include('persona.urls')),
    url(r'^examen/', include('imaging.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^admision/', include('spital.urls')),
    url(r'^enfermeria/', include('nightingale.urls')),
    url(r'^consultorio/', include('clinique.urls')),
    url(r'^income/', include('income.urls')),
    url(r'^caja/', include('invoice.urls')),
    url(r'^emergencia/', include('emergency.urls')),
    url(r'^contracts/', include('contracts.urls')),
    url(r'^lab/', include('lab.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^rrhh/', include('bsc.urls')),
    url(r'^rrhh/', include('bsc.urls', namespace='bsc')),
    url(r'^budget/', include('budget.urls')),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
        profile_edit,
        {'edit_profile_form': CustomEditProfileForm},
        name='userena_profile_edit'),
    url(r'^accounts/signin',
        views.SigninPathAction,
        name='user-signin-path'),
    url(r'^accounts/', include('userena.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += (url(r'^__debug__/', include(debug_toolbar.urls)),)
