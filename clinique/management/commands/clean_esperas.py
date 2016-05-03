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
from django.utils import timezone

from clinique.models import Espera


class Command(BaseCommand):
    """
    Cleans old :class:`Espera`s to avoid them showing up in the UI
    """
    help = "Cleans up the old Espera by marking them as absent."

    def handle(self, *args, **options):

        Espera.objects.pendientes().filter(
            created__year__lt=timezone.now().year
        ).update(ausente=True)
