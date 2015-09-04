# -*- coding: utf-8 -*-
from django.contrib import admin

from users.models import Ciudad, Company

# admin.site.register(UserProfile)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rtn', 'cai')
    ordering = ['nombre', 'rtn', 'cai']
    search_fields = ['nombre', 'rtn', 'cai']


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                    'correlativo_de_comprobante', 'prefijo_comprobante')
    ordering = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                'correlativo_de_comprobante', 'prefijo_comprobante']
    search_fields = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo',
                     'correlativo_de_comprobante', 'prefijo_comprobante']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Ciudad, CiudadAdmin)
