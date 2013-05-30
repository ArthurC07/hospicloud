# -*- coding: utf-8 -*-
#
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

from spital.models import Admision, Habitacion, PreAdmision
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authentication import (ApiKeyAuthentication, MultiAuthentication,
                                     SessionAuthentication, Authentication)
from tastypie.resources import ModelResource
from tastypie import fields

class AdmisionResource(ModelResource):
    paciente = fields.ForeignKey('persona.api.PersonaResource', 'paciente', full=True)
    habitacion = fields.ForeignKey('spital.api.HabitacionResource', 'habitacion', full=True)
    
    class Meta:
        
        queryset = Admision.objects.all()
        authorization = ReadOnlyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(),
                                             Authentication(),
                                             ApiKeyAuthentication())

class HabitacionResource(ModelResource):
    
    class Meta:
        
        queryset = Habitacion.objects.all()
        authorization = ReadOnlyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(),
                                             Authentication(),
                                             ApiKeyAuthentication())
