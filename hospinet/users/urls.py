# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from users.views import UserPersonaCreateView, UserPersonaUpdateView, \
    UserFisicoUpdateView, UserAntecedenteObstetricoUpdateView, \
    UserAntecedenteUpdateView, UserAntecedenteFamiliarUpdateView, \
    UserAntecedenteQuirurgicoUpdateView, UserEstiloVidaUpdateView

urlpatterns = patterns('',
                       url(r'^profile/persona/add$',
                           UserPersonaCreateView.as_view(),
                           name='user-persona-create'),

                       url(r'^profile/persona/(?P<pk>\d+)/editar$',
                           UserPersonaUpdateView.as_view(),
                           name='user-persona-edit'),

                       url(r'^(?P<pk>\d+)/fisico/editar$',
                           UserFisicoUpdateView.as_view(),
                           name='user-fisico-editar'),

                       url(r'^(?P<pk>\d+)/estilovida/editar$',
                           UserEstiloVidaUpdateView.as_view(),
                           name='user-estilovida-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/editar$',
                           UserAntecedenteUpdateView.as_view(),
                           name='user-antecedente-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
                           UserAntecedenteFamiliarUpdateView.as_view(),
                           name='user-antecedente-familiar-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
                           UserAntecedenteQuirurgicoUpdateView.as_view(),
                           name='user-antecedente-quirurgico-editar'),

                       url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
                           UserAntecedenteObstetricoUpdateView.as_view(),
                           name='user-antecedente-obstetrico-editar'),
)
