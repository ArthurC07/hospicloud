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

from django.contrib import admin
from imaging.models import (Examen, Imagen, Adjunto, Dicom, EstudioProgramado,
                            TipoExamen, Estudio, Radiologo, Tecnico)

admin.site.register(Examen)
admin.site.register(Imagen)
admin.site.register(Adjunto)
admin.site.register(Dicom)
admin.site.register(EstudioProgramado)
admin.site.register(TipoExamen)
admin.site.register(Estudio)
admin.site.register(Radiologo)
admin.site.register(Tecnico)
