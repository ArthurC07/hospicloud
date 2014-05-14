# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Carlos Flores <cafg10@gmail.com>
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
from django.db import models
from django_extensions.db.models import TimeStampedModel
from persona.models import Persona


class Resultado(TimeStampedModel):
    """Permite registrar los :class:`Resultado`s de un examen de laboratorio"""

    class Meta:
        permissions = (
            ('lab', 'Permite al usuario administrar laboratorios'),
        )
    persona = models.ForeignKey(Persona, related_name='resultados')
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='lab/results/%Y/%m/%d')

    def get_absolute_url(self):
        """Obtiene la direccion que se utilizará para redireccionar luego de
        o editar un :class:`Resultado`"""

        return self.persona.get_absolute_url()
