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

from django.contrib import admin
from clinique.models import (Paciente, Cita, Consulta, TipoConsulta,
                             Consultorio, Evaluacion, Seguimiento, LecturaSignos,
                             TipoCargo, Cargo, OrdenMedica)

admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Consulta)
admin.site.register(TipoConsulta)
admin.site.register(Consultorio)
admin.site.register(Seguimiento)
admin.site.register(Evaluacion)
admin.site.register(LecturaSignos)
admin.site.register(OrdenMedica)
admin.site.register(Cargo)
admin.site.register(TipoCargo)
