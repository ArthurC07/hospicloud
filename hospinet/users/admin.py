# -*- coding: utf-8 -*-
from django.contrib import admin

from users.models import Ciudad

# admin.site.register(UserProfile)


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correlativo', 'prefijo_recibo')
    ordering = ['nombre', 'correlativo', 'prefijo_recibo']
    search_fields = ['nombre', 'correlativo', 'prefijo_recibo']


admin.site.register(Ciudad, CiudadAdmin)
