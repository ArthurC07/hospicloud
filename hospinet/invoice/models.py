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
from collections import defaultdict
from decimal import Decimal

from constance import config
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from persona.models import Persona
from inventory.models import ItemTemplate, TipoVenta
from spital.models import Deposito


dot01 = Decimal("0.01")


class TipoPago(TimeStampedModel):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.nombre


class Recibo(TimeStampedModel):
    """Permite registrar pagos por productos y servicios"""

    class Meta:
        permissions = (
            ('cajero', 'Permite al usuario gestionar caja'),
        )

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

    def numero(self):

        return config.INVOICE_OFFSET + self.id

    def anular(self):

        """Anula el :class:`Recibo` para que no se tome en cuenta en los
        calculos financieros"""

        self.nulo = True
        for pago in self.pagos.all():
            pago.delete()
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
        return Decimal(subtotal).quantize(dot01)

    def impuesto(self):

        """Calcula los impuestos que se deben pagar por este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        tax = sum(v.tax() for v in self.ventas.all())
        return Decimal(tax).quantize(dot01)

    def descuento(self):

        """Calcula el descuento que se debe restar a este :class:`Recibo`"""

        if self.nulo:
            return Decimal(0)

        discount = sum(v.discount() for v in self.ventas.all())
        return Decimal(discount).quantize(dot01)

    def conceptos(self):

        return ', '.join(v.item.descripcion for v in self.ventas.all())

    def total(self):

        """Calcula el monto que será mostrado en los cálculos financieros"""

        if self.nulo:
            return Decimal(0)

        total = sum(v.total() for v in self.ventas.all())
        return Decimal(total).quantize(dot01)

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

    def pagado(self):

        return sum(p.monto for p in self.pagos.all())

    def debido(self):

        return self.total() - self.pagado()


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
            return self.precio.quantize(dot01)

        aumento = self.recibo.tipo_de_venta.incremento * self.precio
        return (self.precio + aumento).quantize(dot01)

    def precio_previo(self):

        if not self.recibo.tipo_de_venta:
            return self.precio.quantize(dot01)

        aumento = self.recibo.tipo_de_venta.incremento * self.precio
        return (self.precio + aumento).quantize(dot01)

    def descuento_tipo(self):

        if not self.recibo.tipo_de_venta or not self.descontable:
            return Decimal(0)

        disminucion = self.recibo.tipo_de_venta.disminucion * self.cantidad
        return (self.precio_unitario() * disminucion).quantize(dot01)

    def tax(self):
        """Obtiene los impuestos a pagar por esta :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return ((self.monto() - self.discount()) * self.impuesto).quantize(
            dot01)

    def total(self):
        """Calcula el valor total de esta :class:`Venta`"""

        if self.recibo.nulo:
            return Decimal(0)

        return (self.tax() + self.monto() - self.descuento_tipo()).quantize(
            dot01)

    def discount(self):

        """Calcula la cantidad que se disminuye de la :class:`Venta`"""

        return self.descuento_tipo()

    def radiologo(self):

        """Calcular las comisiones del radiologo que atiende tomando en cuenta
        los descuentos que se han efectuado al recibo"""

        if self.recibo.radiologo is None or self.recibo.radiologo == '':
            return Decimal('0')

        bruto = self.monto() * self.item.comision / Decimal("100")
        neto = bruto - bruto * self.descuento / Decimal("100")

        return neto.quantize(dot01)


class Pago(TimeStampedModel):
    """Permite especificar los montos de acuerdo al :class:`TipoPago` utilizado
    por el cliente para pagar el :class:`Recibo`"""

    tipo = ForeignKey(TipoPago, related_name='pagos')
    recibo = ForeignKey(Recibo, related_name='pagos')
    monto = models.DecimalField(blank=True, null=True, max_digits=7,
                                decimal_places=2)
    comprobante = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "Pago en {2} de {0} al recibo {1}".format(self.monto,
                                                         self.recibo.id,
                                                         self.tipo.nombre)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-view-id', args=[self.recibo.id])


class TurnoCaja(TimeStampedModel):
    usuario = models.ForeignKey(User, related_name='turno_caja')
    inicio = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)
    apertura = models.DecimalField(blank=True, null=True, max_digits=7,
                                   decimal_places=2)
    finalizado = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Turno de {0} del {1} al {2}".format(
            self.usuario.get_full_name(),
            self.inicio, self.fin)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-turno', args=[self.id])

    def recibos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Recibo.objects.filter(cajero=self.usuario,
                                     created__gte=self.inicio,
                                     created__lte=fin).all()

    def depositos(self):

        fin = self.fin
        if fin is None:
            fin = timezone.now()

        return Deposito.objects.filter(created__gte=self.inicio,
                                       created__lte=fin).all()

    def venta(self):

        return sum(r.total() for r in self.recibos())

    def depositado(self):

        return sum(d.monto for d in self.depositos())

    def ingresos(self):
        return sum(r.pagado() for r in self.recibos())

    def pagos(self):

        metodos = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            metodos[tipo] = 0

        for recibo in self.recibos():

            for pago in recibo.pagos.all():
                metodos[pago.tipo] += pago.monto

        return metodos.iteritems()

    def total_cierres(self):

        return sum(c.monto for c in self.cierres.all())

    def diferencia(self):

        metodos = defaultdict(Decimal)
        for recibo in self.recibos():

            for pago in recibo.pagos.all():
                metodos[pago.tipo] += pago.monto

        cierres = defaultdict(Decimal)
        for cierre in self.cierres.all():
            cierres[cierre.pago] += cierre.monto

        diferencia = defaultdict(Decimal)
        for tipo in TipoPago.objects.all():
            diferencia[tipo] = cierres[tipo] - metodos[tipo]

        return diferencia.iteritems()

    def diferencia_total(self):

        cierre = sum(c.monto for c in self.cierres.all())
        pagos = sum(r.pagado() for r in self.recibos())

        return cierre - pagos - self.apertura


class CierreTurno(TimeStampedModel):
    turno = models.ForeignKey(TurnoCaja, related_name='cierres')
    pago = models.ForeignKey(TipoPago, related_name='cierres')
    monto = models.DecimalField(blank=True, null=True, max_digits=7,
                                decimal_places=2)

    def get_absolute_url(self):
        """Obtiene la URL absoluta"""

        return reverse('invoice-turno', args=[self.turno.id])

