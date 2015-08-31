from lab.views import IndexView, ResultadoCreateView
from persona.views import PersonaSearchView

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('',

                       url(r'^$',
                           IndexView.as_view(),
                           name='lab-index'),

                       url(r'^resultado/(?P<persona>\d+)/agregar$',
                           ResultadoCreateView.as_view(),
                           name='lab-result-add'),

                       url(r'^buscar$',
                           PersonaSearchView.as_view(
                               template_name='lab/persona_search.html'),
                           name='lab-search'),

                       )
