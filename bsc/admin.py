# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from django_extensions.admin import ForeignKeyAutocompleteAdmin
from bsc.models import Meta, ScoreCard, Escala, Extra, Encuesta, Opcion, \
    Pregunta, Holiday, Login, Puntuacion, Queja, Evaluacion


class MetaAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('score_card', 'tipo_meta', 'peso', 'meta', 'activa')
    ordering = ['score_card', 'tipo_meta', 'peso', 'meta', 'activa']


class EscalaAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('score_card', 'puntaje_inicial', 'puntaje_final', 'comision')
    ordering = ['score_card', 'puntaje_inicial', 'puntaje_final', 'comision']


class ExtraAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('score_card', 'inicio_de_rango', 'fin_de_rango', 'comision')
    ordering = ['score_card', 'inicio_de_rango', 'fin_de_rango', 'comision']


class OpcionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('respuesta', 'pregunta', 'valor')
    ordering = ['respuesta', 'pregunta', 'valor']


class PreguntaAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('encuesta', 'pregunta')
    ordering = ['encuesta', 'pregunta']


class HolidayAdmin(admin.ModelAdmin):
    list_display = ['day']
    ordering = ['day']


class LoginAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['user', 'created', 'holiday']
    ordering = ['user', 'created', 'holiday']


class PuntuacionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['usuario', 'extra', 'fecha', 'puntaje']
    ordering = ['fecha', 'extra', 'usuario', 'puntaje']


class EvaluacionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['usuario', 'meta', 'fecha', 'puntaje']
    ordering = ['fecha', 'extra', 'usuario', 'puntaje']


class QuejaAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['respuesta', 'get_usuario', 'queja', 'resuelta', 'created']
    ordering = ['queja', 'resuelta', 'resuelta', 'created']

    def get_usuario(self, object):

        return object.respuesta.consulta.consultorio.usuario.get_full_name()


admin.site.register(Meta, MetaAdmin)
admin.site.register(ScoreCard)
admin.site.register(Escala, EscalaAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Encuesta)
admin.site.register(Opcion, OpcionAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(Login, LoginAdmin)
admin.site.register(Puntuacion, PuntuacionAdmin)
admin.site.register(Queja, QuejaAdmin)
admin.site.register(Evaluacion, EvaluacionAdmin)
