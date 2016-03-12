# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2016 Carlos Flores <cafg10@gmail.com>
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
from __future__ import unicode_literals

from django.contrib import admin

from users.models import Ciudad, Company, Turno


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rtn', 'cai')
    ordering = ['nombre', 'rtn', 'cai']
    search_fields = ['nombre', 'rtn', 'cai']


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                    'correlativo_de_comprobante', 'prefijo_comprobante',
                    'cai_recibo', 'cai_comprobante')
    ordering = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                'correlativo_de_comprobante', 'prefijo_comprobante']
    search_fields = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                     'correlativo_de_comprobante', 'prefijo_comprobante']


class TurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'inicio', 'fin', 'contabilizable']
    filter_horizontal = ('usuarios',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Turno, TurnoAdmin)
