# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns,  url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login.djhtml'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
)
