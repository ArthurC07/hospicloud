# -*- coding: utf-8 -*-
from django.contrib import admin

from users.models import Ciudad, Company

# admin.site.register(UserProfile)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rtn', 'cai')
    ordering = ['nombre', 'rtn', 'cai']
    search_fields = ['nombre', 'rtn', 'cai']


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correlativo_de_recibo', 'prefijo_recibo')
    ordering = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo']
    search_fields = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Ciudad, CiudadAdmin)
