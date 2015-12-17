# -*- coding: utf-8 -*-
from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^profile/persona/add$',
        views.UserPersonaCreateView.as_view(),
        name='user-persona-create'),

    url(r'^profile/persona/(?P<pk>\d+)/editar$',
        views.UserPersonaUpdateView.as_view(),
        name='user-persona-edit'),

    url(r'^(?P<pk>\d+)/fisico/editar$',
        views.UserFisicoUpdateView.as_view(),
        name='user-fisico-edit'),

    url(r'^(?P<pk>\d+)/estilovida/editar$',
        views.UserEstiloVidaUpdateView.as_view(),
        name='user-estilovida-edit'),

    url(r'^(?P<pk>\d+)/antecedente/editar$',
        views.UserAntecedenteUpdateView.as_view(),
        name='user-antecedente-edit'),

    url(r'^(?P<pk>\d+)/antecedente/familiar/editar$',
        views.UserAntecedenteFamiliarUpdateView.as_view(),
        name='user-antecedente-familiar-edit'),

    url(r'^(?P<pk>\d+)/antecedente/quirurgico/editar$',
        views.UserAntecedenteQuirurgicoUpdateView.as_view(),
        name='user-antecedente-quirurgico-edit'),

    url(r'^(?P<pk>\d+)/antecedente/obstetrico/editar$',
        views.UserAntecedenteObstetricoUpdateView.as_view(),
        name='user-antecedente-obstetrico-edit'),

    url(r'^(?P<persona>\d+)/antecedente/quirurgico/agregar$',
        views.UserAntecedenteQuirurgicoCreateView.as_view(),
        name='user-antecedente-quirurgico-agregar'),
]
