# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from users.views import UserPersonaCreateView, UserPersonaUpdateView, \
    UserFisicoUpdateView, UserAntecedenteObstetricoUpdateView, \
    UserAntecedenteUpdateView, UserAntecedenteFamiliarUpdateView, \
    UserAntecedenteQuirurgicoUpdateView, UserEstiloVidaUpdateView, \
    UserAntecedenteQuirurgicoCreateView

urlpatterns = patterns('',
                       url(r'^profile/persona/add$',
                           UserPersonaCreateView.as_view(),
                           name='user-persona-create'),

                       url(r'^profile/persona/(?P<pk>\d+)/editar$',
                           UserPersonaUpdateView.as_view(),
                           name='user-persona-edit'),

                       url(r'^(?P<pk>\d+)/fisico/editar$',
                           UserFisicoUpdateView.as_view(),
                           name='user-fisico-edit'),

                       url(r'^(?P<pk>\d+)/estilovida/editar$',
                           UserEstiloVidaUpdateView.as_view(),
                           name='user-estilovida-edit'),

                       url(r'^(?P<pk>\d+)/antecedente/editar$',
                           UserAntecedenteUpdateView.as_view(),
                           name='user-antecedente-edit'),

                       url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
                           UserAntecedenteFamiliarUpdateView.as_view(),
                           name='user-antecedente-familiar-edit'),

                       url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
                           UserAntecedenteQuirurgicoUpdateView.as_view(),
                           name='user-antecedente-quirurgico-edit'),

                       url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
                           UserAntecedenteObstetricoUpdateView.as_view(),
                           name='user-antecedente-obstetrico-edit'),

                       url(r'^(?P<persona>\d+)/antecedente/quirurgico/agregar$',
                           UserAntecedenteQuirurgicoCreateView.as_view(),
                           name='user-antecedente-quirurgico-agregar'),
)
