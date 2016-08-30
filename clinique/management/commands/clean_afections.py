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
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from clinique.models import DiagnosticoClinico, Afeccion


class Command(BaseCommand):
    help = _('Deletes all afections from the database')

    def handle(self, *args, **options):
        # First make sure that no Clinical Diagnostic

        print(_('Diagnostics before cleanup {0}'.format(
            DiagnosticoClinico.objects.count()))
        )

        DiagnosticoClinico.objects.all().update(
            afeccion=None
        )

        Afeccion.objects.all().delete()

        print(_('Diagnostics after cleanup {0}'.format(
            DiagnosticoClinico.objects.count()))
        )
