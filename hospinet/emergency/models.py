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
from inventory.models import ItemTemplate

class Emergencia(TimeStampedModel):

    """Representa una visita de una :class:`Persona` a la consulta de
    emergencia"""

    persona = models.ForeignKey(Persona, related_name='emergencias')
    historia_enfermedad_actual = models.TextField(blank=True, null=True)
    pulso = models.IntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True, blank=True)
    presion = models.CharField(max_length=100, null=True, blank=True)
    frecuencia_cardiaca = models.DecimalField(decimal_places=2, max_digits=8,
                                             null=True, blank=True)
    respiracion = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    saturacion_de_oxigeno = models.DecimalField(decimal_places=2, max_digits=8,
                                                null=True, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='emergencias')
    
    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.id])

class Tratamiento(TimeStampedModel):

    """Registra las indiciaciones que la :class:`Persona` debe seguir"""

    emergencia = models.ForeignKey(Emergencia, related_name='tratamientos')
    indicaciones = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_tratamientos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class Diagnostico(TimeStampedModel):

    """Registra el resultado que el medico ha encontrado luego de auscultar
    a la :class:`Persona`"""

    emergencia = models.ForeignKey(Emergencia, related_name='diagnosticos')
    diagnostico = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_diagnosticos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class ExamenFisico(TimeStampedModel):

    """Registra los análisis que se le efectua a la :class:`Persona`"""

    emergencia = models.ForeignKey(Emergencia,
                                related_name='examenes_fisicos')
    orl = models.TextField()
    cardiopulmonar = models.TextField()
    gastrointestinal = models.TextField()
    extremidades = models.TextField()
    otras = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='examenes_fisicos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class Hallazgo(TimeStampedModel):

    emergencia = models.ForeignKey(Emergencia,
                                related_name='hallazgos')
    hallazgo = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='hallazgos')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class RemisionInterna(TimeStampedModel):

    emergencia = models.ForeignKey(Emergencia, related_name='remisiones_internas')
    doctor = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_rinternas')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class RemisionExterna(TimeStampedModel):

    emergencia = models.ForeignKey(Emergencia, related_name='remisiones_externas')
    destino = models.CharField(max_length=100)
    diagnostico = models.TextField()
    notas = models.TextField()
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='er_rexternas')

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergency-view-id', args=[self.emergencia.id])

class Cobro(TimeStampedModel):

    """Permite registrar los distintos cargos"""

    emergencia = models.ForeignKey(Emergencia, related_name='cobros')
    cargo = models.ForeignKey(ItemTemplate, related_name='cobros')
    cantidad = models.IntegerField(default=1)

    def get_absolute_url(self):
        
        """Obtiene la URL absoluta"""
        
        return reverse('emergencia-cobro-agregar', args=[self.emergencia.id])
