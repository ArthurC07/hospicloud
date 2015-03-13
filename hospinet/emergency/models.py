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

from collections import defaultdict

from constance import config
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from persona.models import Persona, transfer_object_to_persona, \
    persona_consolidation_functions
from inventory.models import ItemTemplate, TipoVenta


class Emergencia(TimeStampedModel):
    """Representa una visita de una :class:`Persona` a la consulta de
    emergencia"""

    class Meta:
        permissions = (
            ('emergencia', 'Permite al usuario gestionar emergencia'),
        )

    persona = models.ForeignKey(Persona, related_name='emergencias')
    historia_enfermedad_actual = models.TextField(blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(decimal_places=2, max_digits=8,
                                      null=True, blank=True)
    presion = models.CharField(max_length=100, null=True, blank=True)
    frecuencia_cardiaca = models.DecimalField(decimal_places=2, max_digits=8,
                                              null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    saturacion_de_oxigeno = models.DecimalField(decimal_places=2, max_digits=8,
                                                null=True, blank=True)
    usuario = models.ForeignKey(User, blank=True, null=True,
                                related_name='emergencias')
    facturada = models.NullBooleanField(default=False)
    tipo_de_venta = models.ForeignKey(TipoVenta, blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('emergency-view-id', args=[self.id])

    def tiempo(self):
        ahora = timezone.now()
        delta = ahora - self.created
        hours, remainder = divmod(delta.seconds, 3600)
        return hours

    def facturar(self):
        items = defaultdict(int)

        for cargo in self.cobros.filter(facturado=False).all():
            items[cargo.cargo] += cargo.cantidad
            cargo.facturado = True
            cargo.save()

        horas = self.tiempo()

        emergencia = ItemTemplate.objects.get(pk=config.EMERGENCIA)

        items[emergencia] = 1
        items[self.usuario.profile.honorario] = 1

        if horas >= 1:
            restante = horas - 1
            extra = ItemTemplate.objects.get(pk=config.EXTRA_EMERGENCIA)
            items[extra] = restante
        
        return items

    def total(self):

        return sum(c.total() for c in self.cobros.all())

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
    facturado = models.NullBooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('emergencia-cobro-agregar', args=[self.emergencia.id])

    def __unicode__(self):
        return u'{1}: {0}'.format(self.cargo.descripcion, self.created)

    def total(self):

        return self.cargo.precio_de_venta * self.cantidad


def consolidate_emergency(persona, clone):
    [transfer_object_to_persona(emergency, persona) for emergency in
     clone.emergencias.all()]


persona_consolidation_functions.append(consolidate_emergency)
