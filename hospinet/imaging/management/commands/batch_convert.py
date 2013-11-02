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


from imaging.models import Dicom
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    """Permite convertir todos los DICOM pendientes de conversion"""

    def handle(self, *args, **options):
        dicoms = Dicom.objects.filter(convertido=False)
        map((lambda d: d.extraer_imagen()), dicoms)
