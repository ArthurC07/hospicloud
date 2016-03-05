# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Carlos Flores <cafg10@gmail.com>
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

from decimal import Decimal

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from budget.models import Fuente
from invoice.models import Pago, CuentaPorCobrar
from persona.models import Persona


@python_2_unicode_compatible
class TipoDeposito(TimeStampedModel):
    """
    Indicates the origin of the money that will be used for a :class:`Deposito`
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Banco(TimeStampedModel):
    """
    Represents the banking institution available to :class:`Company`s
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class DepositoQuerySet(models.QuerySet):
    """
    Creates filters for usual :class:`Deposito` :class:`QuerySet`s
    """
    def periodo(self, inicio, fin):
        """
        Returns all :class:`Deposito` with a fecha_de_deposito that falls
        within the specified range.
        """
        return self.filter(fecha_de_deposito__range=(inicio, fin))


@python_2_unicode_compatible
class Deposito(TimeStampedModel):
    """
    Represents money that has been sent to the bank.
    """
    tipo = models.ForeignKey(TipoDeposito, null=True)
    cuenta = models.ForeignKey(Fuente)
    fecha_de_deposito = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    aplicado = models.BooleanField(default=False)
    comprobante = models.FileField(upload_to='income/deposito/%Y/%m/%d')

    objects = DepositoQuerySet.as_manager()

    def __str__(self):

        return self.cuenta.nombre

    def get_absolute_url(self):

        return reverse('income-deposito', args=[self.id])

    def save(self, **kwargs):
        """
        During saving the program increases the money available in the
        :class:`Fuente`
        :param kwargs:
        :return:
        """
        if not self.aplicado:
            self.cuenta.monto += self.monto
            self.aplicado = True

        super(Deposito, self).save(**kwargs)

    def delete(self, **kw):
        """
        During deletion the money available in the :class:`Fuente` decreases
        :param kw:
        :return:
        """
        if self.aplicado:
            self.cuenta.monto -= self.monto
            self.aplicado = False

        super(Deposito, self).delete(**kw)


@python_2_unicode_compatible
class TipoCheque(TimeStampedModel):
    nombre = models.CharField(max_length=255)

    def __str__(self):

        return self.nombre


@python_2_unicode_compatible
class Cheque(TimeStampedModel):
    """
    Represents a cheque that has been sent
    """
    tipo = models.ForeignKey(TipoCheque, null=True)
    banco_de_emision = models.ForeignKey(Banco)
    emisor = models.ForeignKey(Persona, null=True)
    fecha_de_entrega = models.DateTimeField(default=timezone.now)
    fecha_de_emision = models.DateTimeField(default=timezone.now)
    numero_de_cheque = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    monto_retenido = models.DecimalField(max_digits=11, decimal_places=2,
                                         default=0)
    imagen_de_cheque = models.FileField(upload_to='income/cheque/%Y/%m/%d',
                                        null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return _('{0} - {1}').format(
                self.banco_de_emision.nombre,
                self.numero_de_cheque
        )

    def get_absolute_url(self):
        return reverse('cheque-detail', args=[self.id])

    def pendiente(self):
        """
        Calculates how much money is still not liquidated from the
        :class:`Cheque`

        :return: The amount of leftover money
        """
        return self.monto - self.detallepago_set.aggregate(
                total=Coalesce(Sum('monto'), Decimal())
        )['total'] + self.monto_retenido

    def liquidado(self):
        """
        :return: The amount that has been already consolidated
        """

        return self.detallepago_set.aggregate(
                liquidado=Coalesce(Sum('monto'), Decimal())
        )['liquidado']

    def monto_total(self):
        return self.monto + self.monto_retenido


@python_2_unicode_compatible
class CierrePOS(Deposito):
    """
    Describes the closing of the the POS.
    """
    batch = models.CharField(max_length=255)
    banco = models.ForeignKey(Banco)

    def __str__(self):
        return self.banco.nombre


class DetallePago(TimeStampedModel):
    """
    Describes how a :class:`Pago` got liquidated.
    """
    cheque = models.ForeignKey(Cheque, null=True)
    pago = models.ForeignKey(Pago)
    monto = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def get_absolute_url(self):
        return self.cheque.get_absolute_url()

    def save(self, **kwargs):
        """
        Marks the original :class:`Pago` as completed when a
        :class:`DetallePago` is saved.
        :param kwargs:
        :return:
        """
        if self.monto >= self.pago.monto:
            self.pago.completado = True
            self.pago.status = self.pago.status.next_status
            self.pago.save()

        super(DetallePago, self).save(**kwargs)

    def delete(self, **kwargs):
        """
        Removes the completition mark from a :class:`Pago` when a
        :class:`DetallePago` is deleted.
        :param kwargs:
        :return:
        """
        self.pago.completado = False
        self.pago.status = self.pago.status.previous_status
        self.pago.save()

        super(DetallePago, self).delete(**kwargs)
