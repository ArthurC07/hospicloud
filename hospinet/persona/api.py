# -*- coding: utf-8 -*-
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

from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from persona.models import Persona
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authentication import (ApiKeyAuthentication, MultiAuthentication,
                                     SessionAuthentication, Authentication)
from django.forms.models import model_to_dict

class PersonaResource(ModelResource):
    
    class Meta:
        
        queryset = Persona.objects.all()
        authorization = ReadOnlyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(),
                                             Authentication(),
                                             ApiKeyAuthentication())
    
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        return
