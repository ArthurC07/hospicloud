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

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from decimal import Decimal
from persona.models import Persona

class Emergencia(TimeStampedModel):

    """Representa una visita de una :class:`Persona` a la consulta de
    emergencia"""

    persona = models.ForeignKey('Persona', related_name='emergencias')
    hallazgos = models.TextField()
    diagnostico = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_examenes')
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-detail', args=[self.id])

class Tratamiento(TimeStampedModel):

    """Registra las indiciaciones que la :class:`Persona` debe seguir"""

    emergencia = models.ForeignKey('Emergencia', related_name='tratamientos')
    indicaciones = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_tratamientos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-detail', args=[self.emergencia.id])

class RemisionInterna(TimeStampedModel):

    emergencia = models.ForeignKey('Emergencia', related_name='remisiones_internas')
    doctor = models.CharField(max_lenght=100)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_rinternas')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-detail', args=[self.emergencia.id])

class RemisionExterna(TimeStampedModel):

    emergencia = models.ForeignKey('Emergencia', related_name='tratamientos')
    destino = models.CharField(max_lenght=100)
    diagnostico = models.TextField()
    notas = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_rexternas')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-detail', args=[self.emergencia.id])
