# -*- coding: utf-8 -*-
from django.conf.urls import patterns,  url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
)
