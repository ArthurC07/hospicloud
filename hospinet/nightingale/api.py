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

from nightingale.models import Medicamento
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authentication import (ApiKeyAuthentication, MultiAuthentication,
                                     SessionAuthentication, Authentication)
from tastypie.resources import ModelResource
from django.db.models.query_utils import Q
from tastypie import fields


class MedicamentoResource(ModelResource):
    cargo = fields.ForeignKey('inventory.api.ItemTemplateResource', 'cargo', full=True)
    admision = fields.ForeignKey('spital.api.AdmisionResource', 'admision', full=True)

    class Meta:
        queryset = Medicamento.objects.filter(Q(estado=1))
        authorization = ReadOnlyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(),
                                             Authentication(),
                                             ApiKeyAuthentication())
        filtering = {
            'proxima_dosis': ['lte', 'gte', 'gt', 'lt'],
        } 
