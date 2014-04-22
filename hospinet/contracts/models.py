# !/usr/bin/env python
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
import calendar
from datetime import date
import operator

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from clinique.models import Consulta, Seguimiento, Cita

from inventory.models import ItemTemplate
from persona.models import Persona, Empleador


class Vendedor(TimeStampedModel):
    """Indica quien realizo una venta de un :clas:`Contrato`"""
    usuario = models.ForeignKey(User, related_name="vendedores")
    habilitado = models.BooleanField(default=True)

    def __unicode__(self):
        return self.usuario.get_full_name()

    def get_contratos_vendidos(self, fecha, fin):

        return self.contratos.filter(inicio__gte=fecha, cancelado=False,
                                     plan__empresarial=False).filter(inicio__lte=fin)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Paciente`"""

        return reverse('contracts-vendedor', args=[self.id])

    def get_contratos_mes(self):

        now = date.today()
        inicio = date(now.year, now.month, 1)
        fin = date(now.year, now.month,
                         calendar.monthrange(now.year, now.month)[1])
        return self.get_contratos_vendidos(inicio, fin).count()


class Plan(TimeStampedModel):
    """Indica los limites que presenta cada :class:`Contrato`"""

    nombre = models.CharField(max_length=255, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    edad_maxima = models.IntegerField()
    adicionales = models.IntegerField()
    medicamentos = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=0)
    empresarial = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empleador, null=True, blank=True,
                                related_name='planes')

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
    renovacion = models.DateField(null=True, blank=True)
    cancelado = models.BooleanField(default=False)
    empresa = models.ForeignKey(Empleador, blank=True, null=True,
                                related_name='contratos')

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Contrato`"""

        return reverse('contrato', args=[self.id])

    def __unicode__(self):
        return u"Contrato {0} de {1}".format(self.numero,
                                             self.persona.nombre_completo())

    def total_consultas(self):
        """"Obtiene el total de :class:`Consulta` que los usuarios del contrato
        han efectuado"""
        if self.renovacion is None:
            self.renovacion = self.inicio
            self.save()

        consultas = Consulta.objects.filter(
            paciente__persona=self.persona,
            created__gte=self.renovacion).count()
        seguimientos = Seguimiento.objects.filter(
            paciente__persona=self.persona,
            created__gte=self.renovacion).count()
        total = seguimientos + consultas
        predicates = []

        for beneficiario in self.beneficiarios.all():
            predicates.append(Q(paciente__persona=beneficiario.persona))

        seguimientos = Seguimiento.objects.filter(
            created__gte=self.renovacion).filter(reduce(operator.or_,
                                                        predicates)).count()
        consultas = Consulta.objects.filter(
            created__gte=self.renovacion).filter(reduce(operator.or_,
                                                        predicates)).count()
        total += seguimientos + consultas

        return total

    def total_citas(self):
        """Obtiene el total de :class:`Cita`s de un periodo"""
        total = self.persona.citas.count()
        predicates = []

        for beneficiario in self.beneficiarios.all():
            predicates.append(Q(paciente__persona=beneficiario.persona))

        total += Cita.objects.filter(created__gte=self.renovacion).filter(
            reduce(operator.or_, predicates)).count()

        return total

    def total_hospitalizaciones(self):
        total = self.persona.admisiones.filter(ingresado__isnull=False).count()
        total += sum(
            b.persona.admisiones.filter(ingresado__isnull=False).count()
            for b in self.beneficiarios.all())
        return total

    def dias_mora(self):
        """Dias extra que pasaron desde el ultimo pago"""
        ahora = timezone.now().date()
        pago = self.ultimo_pago.date()
        delta = ahora - pago
        dias = delta.days
        if dias < 0:
            dias = 0

        return dias

    def mora(self):
        """Obtiene la cantidad moentaria debida en este :class:`Contrato`"""
        dias = self.dias_mora()
        mora = 0

        if dias >= 1:
            mora = 1

        while dias > 30:
            mora += 1
            dias -= 30

        return mora * self.plan.precio


class Beneficiario(TimeStampedModel):
    persona = models.ForeignKey(Persona, related_name='beneficiarios')
    contrato = models.ForeignKey(Contrato, related_name='beneficiarios')
    inscripcion = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.persona.nombre_completo()

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Beneficiario`"""

        return reverse('contrato', args=[self.contrato.id])


class TipoPago(TimeStampedModel):
    item = models.ForeignKey(ItemTemplate, related_name='tipos_pago')

    def __unicode__(self):
        return self.item.descripcion


class Pago(TimeStampedModel):
    """Registra los montos y las fechas en las que se efectuaron los pagos
    de un :class:`Contrato`"""
    contrato = models.ForeignKey(Contrato, related_name='pagos')
    tipo_de_pago = models.ForeignKey(TipoPago, related_name='pagos', null=True)
    fecha = models.DateTimeField(default=timezone.now())
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion = models.TextField(null=True, blank=True)
    facturar = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Pago`"""

        return reverse('contrato', args=[self.contrato.id])


class TipoEvento(TimeStampedModel):
    nombre = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('contrato-index')


class LimiteEvento(TimeStampedModel):
    """Especifica la cantidad máxima de :class:`Evento` por cada
    :class:`TipoEvento` que son cubiertos por un :class:`Plan`"""
    plan = models.ForeignKey(Plan, related_name='limites')
    tipo_evento = models.ForeignKey(TipoEvento, related_name='limites')
    cantidad = models.IntegerField(default=0)

    def get_absolute_url(self):
        return self.plan.get_absolute_url()

    def __unicode__(self):
        return u"Límite {0} de {1} en plan {2}".format(self.tipo_evento,
                                                       self.cantidad,
                                                       self.plan.nombre)


class Evento(TimeStampedModel):
    """Registra el uso de los beneficios del :class:`Evento`"""
    contrato = models.ForeignKey(Contrato, related_name='eventos')
    tipo = models.ForeignKey(TipoEvento, related_name='eventos')
    fecha = models.DateTimeField(default=timezone.now())
    descripcion = models.TextField(blank=True, null=True)
    adjunto = models.FileField(upload_to='evento/%Y/%m/%d', blank=True,
                               null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):
        """Obtiene la url relacionada con un :class:`Evento`"""

        return reverse('contrato', args=[self.contrato.id])

    def __unicode__(self):
        return "Evento {0} de {1} de {2}".format(self.tipo,
                                                 self.contrato.numero,
                                                 self.contrato.persona.nombre_completo())


class Meta(TimeStampedModel):
    fecha = models.DateField(default=timezone.now())
    contratos = models.IntegerField()

    def get_absolute_url(self):
        """Obtiene la url relacionada con una :class:`Meta`"""

        return reverse('contracts-meta', args=[self.id])


class Cancelacion(TimeStampedModel):
    """Registra las condiciones en las cuales se termina un :class:`Contrato`"""
    contrato = models.ForeignKey(Contrato, related_name='cancelaciones')
    fecha = fecha = models.DateField(default=timezone.now())
    motivo = models.TextField()
    pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_absolute_url(self):

        return self.contrato.get_absolute_url()
