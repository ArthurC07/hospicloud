# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Flores <cafg10@gmail.com>
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

from django.core.management.base import BaseCommand

from persona.models import HistoriaFisica


class Command(BaseCommand):

    def handle(self, *args, **options):

        for historia in HistoriaFisica.objects.all():

            historia.bmi = historia.body_mass_index()
            historia.save()
