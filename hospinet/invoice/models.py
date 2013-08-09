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

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

from persona.models import Persona
from inventory.models import ItemTemplate, TipoVenta


class Recibo(TimeStampedModel):
    """Permite registrar pagos por productos y servicios"""

    cliente = models.ForeignKey(Persona, related_name='recibos')
    remite = models.CharField(max_length=255, blank=True, null=True)
    radiologo = models.CharField(max_length=255, blank=True, null=True)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    cerrado = models.BooleanField(default=False)
    nulo = models.BooleanField(default=False)
    cajero = models.ForeignKey(User, blank=True, null=True,
                               related_name='recibos')
    tipo_de_venta = models.ForeignKey(TipoVenta, blank=True, null=True)

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.id])

    def anular(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.nulo = True
        self.save()

    def cerrar(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.cerrado = True
        self.save()

    def __unicode__(self):

        """Crea una representación en texto del :class:`Recibo`"""

        if self.nulo:
            return u'{0} **NULO**'.format(self.cliente.nombre_completo())

        return self.cliente.nombre_completo()

    def subtotal(self):

        """Calcula el monto antes de impuestos"""

        if self.nulo:
            return Decimal(0)

        subtotal = sum(v.monto() for v in self.ventas.all())
        return Decimal(subtotal).quantize(Decimal('0.01'))

    def impuesto(self):

        """Calcula los impuestos que se deben pagar por este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        tax = sum(v.tax() for v in self.ventas.all())
        return Decimal(tax).quantize(Decimal('0.01'))

    def descuento(self):

        """Calcula el descuento que se debe restar a este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        discount = sum(v.discount() for v in self.ventas.all())
        discount += self.subtotal() * self.discount / Decimal("100")
        return Decimal(discount).quantize(Decimal('0.01'))

    def conceptos(self):

        return ', '.join(v.item.descripcion for v in self.ventas.all())

    def total(self):

        """Calcula el monto que será mostrado en los cálculos financieros"""

        if self.nulo:
            return Decimal(0)

        total = sum(v.total() for v in self.ventas.all())
        return Decimal(total).quantize(Decimal('0.01'))

    def comision_doctor(self):

        return self.total() * Decimal('0.07')

    def comision_radiologo(self):

        return sum(v.radiologo() for v in self.ventas.all())

    def placas(self):

        return sum(v.placas for v in self.ventas.all())

    def fractional(self):
        """Obtiene la parte decimal del total del :class:`Recibo`"""

        return self.total() % 1

    def integer(self):
        """Obtiene la parte entera del total del :class:`Recibo`"""

        return int(self.total())


class Venta(TimeStampedModel):
    """Relaciona :class:`Producto` a un :class:`Recibo` lo cual permite
    realizar los cobros asociados"""

    cantidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(blank=True, null=True, max_digits=7,
                                 decimal_places=2)
    impuesto = models.DecimalField(blank=True, null=True, max_digits=7,
                                   decimal_places=2)
    descuento = models.IntegerField(default=0)
    item = models.ForeignKey(ItemTemplate, related_name='ventas',
                             blank=True, null=True)
    recibo = models.ForeignKey(Recibo, related_name='ventas')
    placas = models.IntegerField(default=0)
    descontable = models.BooleanField(default=True)

    def __unicode__(self):

        return u"{0} a {1}".format(self.item.descripcion, self.recibo.id)

    def get_absolute_url(self):

        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.recibo.id])

    def monto(self):

        """Obtiene el valor a pagar por esta :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return Decimal(self.precio_unitario() * self.cantidad)

    def precio_unitario(self):

        if not self.recibo.tipo_de_venta or not self.descontable:
            return self.precio

        aumento = self.recibo.tipo_de_venta.incremento * self.precio / Decimal(
            100)
        disminucion = self.recibo.tipo_de_venta.disminucion * self.precio / \
                      Decimal(
            100)

        return self.precio + aumento - disminucion

    def precio_previo(self):

        if not self.recibo.tipo_de_venta:
            return self.precio

        aumento = self.recibo.tipo_de_venta.incremento * self.precio / Decimal(
            100)

        return self.precio + aumento

    def descuento_tipo(self):

        if not self.recibo.tipo_de_venta:
            return Decimal(0)

        disminucion = self.recibo.tipo_de_venta.disminucion * self.precio / \
                      Decimal(
            100)
        return disminucion

    def tax(self):

        """Obtiene los impuestos a pagar por esta :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return (self.monto() - self.discount()) * self.impuesto

    def total(self):

        """Calcula el valor total de esta :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return self.tax() + self.monto() - self.discount()

    def discount(self):

        """Calcula la cantidad que se disminuye de la :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return self.monto() * self.descuento / Decimal("100")

    def radiologo(self):

        """Calcular las comisiones del radiologo que atiende tomando en cuenta
        los descuentos que se han efectuado al recibo"""

        if self.recibo.radiologo == None or self.recibo.radiologo == '':
            return Decimal('0')

        bruto = self.monto() * self.item.comision / Decimal("100")
        neto = bruto - bruto * self.descuento / Decimal("100")

        return neto.quantize(Decimal('0.01'))
