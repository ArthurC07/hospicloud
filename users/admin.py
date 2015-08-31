# -*- coding: utf-8 -*-
from django.contrib import admin

from users.models import Ciudad

# admin.site.register(UserProfile)


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correlativo_de_recibo', 'prefijo_recibo')
    ordering = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo']
    search_fields = ['nombre', 'correlativo_de_recibo', 'prefijo_recibo']


admin.site.register(Ciudad, CiudadAdmin)
