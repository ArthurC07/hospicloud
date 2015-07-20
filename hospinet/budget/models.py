# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2015 Carlos Flores <cafg10@gmail.com>
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

from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.models import TimeStampedModel
from users.models import Ciudad


@python_2_unicode_compatible
class Presupuesto(TimeStampedModel):
    """Define un presupuesto financiero para una :class:`Ciudad` específica"""
    ciudad = models.ForeignKey(Ciudad)

    def __str__(self):

        return u'Presupuesto de {0}'.format(self.ciudad.nombre)

@python_2_unicode_compatible
class Cuenta(TimeStampedModel):
    """Define una agrupación de gastos referentes a un rubro determinado"""
    presupuesto = models.ForeignKey(Presupuesto)
    nombre = models.CharField(max_length=255)
    limite = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):

        return self.nombre

@python_2_unicode_compatible
class Gasto(TimeStampedModel):
    """Representa las transacciones monetarias realizadas por el personal de la
    :class:`Ciudad` y que son restadas del :class:`Presupuesto` vigente"""
    cuenta = models.ForeignKey(Cuenta)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):

        return self.descripcion
