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
from nightingale.models import (SignoVital, Evolucion, Cargo, OrdenMedica,
                                Ingesta, Excreta, Glucosuria, Glicemia,
                                Insulina, Sumario, Medicamento,
                                FrecuenciaLectura, NotaEnfermeria, Honorario,
                                OxigenoTerapia)

admin.site.register(SignoVital)
admin.site.register(Evolucion)
admin.site.register(Cargo)
admin.site.register(OrdenMedica)
admin.site.register(Ingesta)
admin.site.register(Excreta)
admin.site.register(Insulina)
admin.site.register(Glicemia)
admin.site.register(Glucosuria)
admin.site.register(Sumario)
admin.site.register(FrecuenciaLectura)
admin.site.register(Medicamento)
admin.site.register(NotaEnfermeria)
admin.site.register(OxigenoTerapia)
admin.site.register(Honorario)
