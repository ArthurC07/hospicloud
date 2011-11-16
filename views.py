# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from haystack.views import SearchView
from library.protected import LoginRequiredView

class IndexView(TemplateView):
    
    template_name = 'index.djhtml'

class CustomSearchView(SearchView, LoginRequiredView):
    
    template_name = 'search/search.html'
