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
from bsc.models import Meta, ScoreCard


class MetaAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('score_card', 'tipo', 'peso', 'meta')
    ordering = ['score_card', 'tipo', 'peso', 'meta']


admin.site.register(Meta, MetaAdmin)
admin.site.register(ScoreCard)
