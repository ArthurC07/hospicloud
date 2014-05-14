from lab.views import IndexView, ResultadoCreateView

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('',

                       url(r'^$',
                           IndexView.as_view(),
                           name='lab-index'),

                       url(r'^resultado(?P<persona>\d+)/agregar$',
                           ResultadoCreateView.as_view(),
                           name='lab-result-add'),

                       )
