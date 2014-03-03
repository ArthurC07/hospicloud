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

from tastypie.api import Api
from persona.api import PersonaResource
from nightingale.api import MedicamentoResource
from inventory.api import ItemTemplateResource
from spital.api import AdmisionResource, HabitacionResource
from users.api import UserResource

v1_api = Api(api_name='mobile')
v1_api.register(PersonaResource())
v1_api.register(MedicamentoResource())
v1_api.register(ItemTemplateResource())
v1_api.register(AdmisionResource())
v1_api.register(HabitacionResource())
v1_api.register(UserResource())
