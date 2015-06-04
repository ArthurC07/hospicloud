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
from emergency.models import (Emergencia, Tratamiento, RemisionInterna,
                              RemisionExterna, Hallazgo, Diagnostico,
                              ExamenFisico, Cobro)


class EmergenciaAdmin(admin.ModelAdmin):
    list_display = ('persona', 'usuario', 'facturada', 'created',)
    ordering = ['persona', 'usuario', 'facturada', 'created']
    search_fields = ['persona__nombre', 'persona__apellido']


admin.site.register(Emergencia, EmergenciaAdmin)
admin.site.register(Tratamiento)
admin.site.register(Hallazgo)
admin.site.register(RemisionInterna)
admin.site.register(RemisionExterna)
admin.site.register(Diagnostico)
admin.site.register(ExamenFisico)
admin.site.register(Cobro)
