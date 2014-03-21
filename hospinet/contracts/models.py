#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2014 Carlos Flores <cafg10@gmail.com>
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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from persona.models import Persona


class Vendedor(TimeStampedModel):
    """Indica quien realizo una venta de un :clas:`Contrato`"""
    usuario = models.ForeignKey(User, related_name="vendedores")
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.usuario.get_full_name()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('contracts-vendedor', args=[self.id])


class Plan(TimeStampedModel):
    """Indica los limites que presenta cada :class:`Contrato`"""

    nombre = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    eventos_maximos = models.IntegerField()
    edad_maxima = models.IntegerField()
    adicionales = models.IntegerField()
    medicamentos = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=0)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Plan`"""

        return reverse('contracts-plan', args=[self.id])


class Contrato(TimeStampedModel):
    """Almacena el estado de cada contrato que se ha celebrado"""

    class Meta:
        permissions = (
            ('contrato', 'Permite al usuario gestionar contratos'),
        )

    persona = models.ForeignKey(Persona, related_name='contratos')
    numero = models.IntegerField()
    vendedor = models.ForeignKey(Vendedor, related_name='contratos')
    plan = models.ForeignKey(Plan, related_name='contratos')
    inicio = models.DateField()
    vencimiento = models.DateField()
    ultimo_pago = models.DateTimeField(default=timezone.now())
    administradores = models.ManyToManyField(User, related_name='contratos',
                                             blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Contrato`"""

        return reverse('contrato', args=[self.id])

    def __unicode__(self):
        return u"Contrato {0} de {1}".format(self.numero,
                                             self.persona.nombre_completo())


class Beneficiario(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='beneficiarios')
    contrato = models.ForeignKey(Contrato, related_name='beneficiarios')
    inscripcion = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Beneficiario`"""

        return reverse('contrato', args=[self.contrato.id])


class Pago(TimeStampedModel):
    """Registra los montos y las fechas en las que se efectuaron los pagos
    de un :class:`Contrato`"""
    contrato = models.ForeignKey(Contrato, related_name='pagos')
    fecha = models.DateTimeField(default=timezone.now())
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Pago`"""

        return reverse('contrato', args=[self.contrato.id])


class TipoEvento(TimeStampedModel):
    nombre = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):

        return reverse('contrato-index')


class Evento(TimeStampedModel):
    """Registra el uso de los beneficios del :class:`Evento`"""
    contrato = models.ForeignKey(Contrato, related_name='eventos')
    tipo = models.ForeignKey(TipoEvento, related_name='eventos')
    fecha = models.DateTimeField(default=timezone.now())
    descripcion = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('contrato', args=[self.contrato.id])

    def __unicode__(self):
        return "Evento {0} de {1} de {2}".format(self.tipo,
                                                 self.contrato.numero,
                                                 self.contrato.persona.nombre_completo())
